from dataclasses import field, fields
from rest_framework import serializers
from .models import Artist, Music


class ArtistListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = ('id','name',)


class MusicListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = ('id','title',)
        read_only_fields = ('artist',)

class ArtistSerializer(serializers.ModelSerializer):
    music_set = MusicListSerializer(read_only=True, many=True)
    music_count = serializers.IntegerField(source='music_set.count', read_only=True)
    class Meta:
        model = Artist
        fields = '__all__'


class MusicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Music
        fields = '__all__'
        read_only_fields = ('artist',)