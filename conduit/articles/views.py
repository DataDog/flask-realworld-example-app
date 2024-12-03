# coding: utf-8

import datetime as dt

from flask import Blueprint
from flask import jsonify
from flask import request
from flask_apispec import marshal_with
from flask_apispec import use_kwargs
from flask_jwt_extended import current_user
from flask_jwt_extended import jwt_required
from marshmallow import fields

from conduit.exceptions import InvalidUsage
from conduit.user.models import User

from .models import Article
from .models import Comment
from .models import Tags
from .serializers import article_schema
from .serializers import articles_schema
from .serializers import comment_schema
from .serializers import comments_schema


blueprint = Blueprint("articles", __name__)


##########
# Articles
##########


@use_kwargs(
    {
        "tag": fields.Str(),
        "author": fields.Str(),
        "favorited": fields.Str(),
        "limit": fields.Int(),
        "offset": fields.Int(),
    }
)
@blueprint.route("/api/articles", methods=("GET",))
@jwt_required(optional=True)
def get_articles(tag=None, author=None, favorited=None, limit=20, offset=0):
    res = Article.query
    if tag:
        res = res.filter(Article.tagList.any(Tags.tagname == tag))
    if author:
        res = res.join(Article.author).join(User).filter(User.username == author)
    if favorited:
        res = res.join(Article.favoriters).filter(User.username == favorited)
    return articles_schema.dump(res.offset(offset).limit(limit).all())


@blueprint.route("/api/articles", methods=("POST",))
@jwt_required()
def make_article(**kwargs):
    data = request.get_json()
    body = data["article"]["body"]
    title = data["article"]["title"]
    description = data["article"]["description"]
    tagList = data["article"]["tagList"]
    article = Article(title=title, description=description, body=body, author=current_user.profile)
    if tagList is not None:
        for tag in tagList:
            mtag = Tags.query.filter_by(tagname=tag).first()
            if not mtag:
                mtag = Tags(tag)
                mtag.save()
            article.add_tag(mtag)
    article.save()
    return article_schema.dump(article)


@use_kwargs(article_schema)
@marshal_with(article_schema)
@blueprint.route("/api/articles/<slug>", methods=("PUT",))
@jwt_required()
def update_article(slug, **kwargs):
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.update(updatedAt=dt.datetime.utcnow(), **kwargs)
    article.save()
    return article_schema.dump(article)


@blueprint.route("/api/articles/<slug>", methods=("DELETE",))
@jwt_required(optional=True)
def delete_article(slug):
    article = Article.query.filter_by(slug=slug, author_id=current_user.profile.id).first()
    article.delete()
    return "", 200


@marshal_with(article_schema)
@blueprint.route("/api/articles/<slug>", methods=("GET",))
@jwt_required(optional=True)
def get_article(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    return article_schema.dump(article)


@marshal_with(article_schema)
@blueprint.route("/api/articles/<slug>/favorite", methods=("POST",))
@jwt_required()
def favorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.favourite(profile)
    article.save()
    return article_schema.dump(article)


@marshal_with(article_schema)
@blueprint.route("/api/articles/<slug>/favorite", methods=("DELETE",))
@jwt_required()
def unfavorite_an_article(slug):
    profile = current_user.profile
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    article.unfavourite(profile)
    article.save()
    return article_schema.dump(article)


@use_kwargs({"limit": fields.Int(), "offset": fields.Int()})
@marshal_with(articles_schema)
@blueprint.route("/api/articles/feed", methods=("GET",))
@jwt_required()
def articles_feed(limit=20, offset=0):
    return (
        Article.query.join(current_user.profile.follows)
        .order_by(Article.createdAt.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )


######
# Tags
######


@blueprint.route("/api/tags", methods=("GET",))
def get_tags():
    return jsonify({"tags": [tag.tagname for tag in Tags.query.all()]})


##########
# Comments
##########


@marshal_with(comments_schema)
@blueprint.route("/api/articles/<slug>/comments", methods=("GET",))
def get_comments(slug):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    return article.comments


@use_kwargs(comment_schema)
@marshal_with(comment_schema)
@blueprint.route("/api/articles/<slug>/comments", methods=("POST",))
@jwt_required()
def make_comment_on_article(slug, **kwargs):
    data = request.get_json()
    body = data["comment"]["body"]
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()
    comment = Comment(article, current_user.profile, body, **kwargs)
    comment.save()
    return comment_schema.dump(comment)


@blueprint.route("/api/articles/<slug>/comments/<cid>", methods=("DELETE",))
@jwt_required()
def delete_comment_on_article(slug, cid):
    article = Article.query.filter_by(slug=slug).first()
    if not article:
        raise InvalidUsage.article_not_found()

    comment = article.comments.filter_by(id=cid, author=current_user.profile).first()
    comment.delete()
    return "", 200
