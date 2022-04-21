from django.shortcuts import render,get_object_or_404, get_list_or_404
from .models import Artist, Music
from .serializers import ArtistListSerializer, ArtistSerializer, MusicListSerializer, MusicSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from music import serializers
# Create your views here.


@api_view(['GET','POST'])
def artists_list(request):
    if request.method=='GET':
        artists = get_list_or_404(Artist)
        serializer = ArtistListSerializer(artists, many=True)
        return Response(serializer.data)

    elif request.method=='POST':
        serializer = ArtistSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
def artist(request,artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    serializer = ArtistSerializer(artist)
    return Response(serializer.data)



@api_view(['POST'])
def artist_music(request,artist_pk):
    artist = get_object_or_404(Artist, pk=artist_pk)
    serializer = MusicSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(artist=artist)
        return Response(serializer.data)



@api_view(['GET'])
def music_list(request):
    musics = get_list_or_404(Music)
    serializer = MusicListSerializer(musics, many=True)
    return Response(serializer.data)


@api_view(['GET','PUT','DELETE'])
def music(request,music_pk):
    music = get_object_or_404(Music,pk=music_pk)
    if request.method=='GET':
        serializer = MusicSerializer(music)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer = MusicSerializer(music, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(serializer.data)

    elif request.method=='DELETE':
        music.delete()
        data = {
            'delete' : f'{music_pk}번 음악이 삭제되었습니다',
        }
        return Response(data, status=status.HTTP_204_NO_CONTENT)