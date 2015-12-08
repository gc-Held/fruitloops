from rest_framework import serializers

from .models import PageActiveTime, BlackListedPages,UserDetails


class BlackListPagesSerializer(serializers.ModelSerializer):
    class Meta:
        model= BlackListedPages
        fields = (
        'user_id',
        'base_url',
        )


class PageActiveTimeSerializer(serializers.ModelSerializer):

    class Meta:

        model = PageActiveTime
        fields = (
            'user_id',
            'page_id',
            'page_title',
            'base_url',
            'cumulative_time',
            'icon_url',
            'last_updated_timestamp',
            'is_active',
            'is_deleted',
            'page_content',
            )

class UserDetailsSerializer(serializers.ModelSerializer):

    class Meta:

        model = UserDetails
        fields = (
            'user_id',
            'email',
            'password',
            'last_login',
            'is_active',
            'is_deleted',
            )

