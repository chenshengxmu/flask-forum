#!/usr/bin/env python
"""Test script for service layer"""
from app import create_app
from app.services.category_service import CategoryService
from app.services.post_service import PostService

app = create_app()

with app.app_context():
    # Test category service
    print("Testing CategoryService...")
    stats = CategoryService.get_all_with_stats()
    print(f"✓ Found {len(stats)} categories with stats")

    if stats:
        stat = stats[0]
        print(f"  - Category: {stat['category'].name}")
        print(f"  - Post count: {stat['post_count']}")
        print(f"  - Latest post: {stat['latest_post']}")

    # Test post service
    print("\nTesting PostService...")
    from app.models import Post
    post = Post.query.first()
    if post:
        post_with_relations = PostService.get_by_id_with_relations(post.id)
        print(f"✓ Loaded post: {post_with_relations.title}")
        print(f"  - Author: {post_with_relations.author.username}")
        print(f"  - Category: {post_with_relations.category.name}")

        replies_data = PostService.get_replies_paginated(post.id, page=1, per_page=10)
        print(f"✓ Loaded {len(replies_data['replies'])} replies (total: {replies_data['total']})")
    else:
        print("  No posts found in database")

    print("\n✅ All service tests passed!")
