from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.shortcuts import redirect
import json
from watson_developer_cloud import ToneAnalyzerV3
from watson_developer_cloud import LanguageTranslatorV2 as LanguageTranslator
from watson_developer_cloud import PersonalityInsightsV3
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
  import Features, EntitiesOptions, KeywordsOptions


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    tone_analyzer = ToneAnalyzerV3(
        username='f6fa4a63-5f86-4c61-9d63-3976d446c393',
        password='oWKMRNBPAhdy',
        version='2016-05-19 ')

    language_translator = LanguageTranslator(
        username='8b8d01c3-a816-43c2-91c0-89070fdd3672',
        password='w142M6bo3krn')

    personality_insights = PersonalityInsightsV3(
        version='2016-10-20',
        username='a5a2fc67-a9fa-43f3-b820-a24238e372a5',
        password='CK0sKUcSkHd8')

    natural_language_understanding = NaturalLanguageUnderstandingV1(
        username='92d06b0d-d197-4686-8ac8-b6d9a449b5fb',
        password='UclOwSkBSuYr',
        version='2018-03-16')

    # print(json.dumps(translation, indent=2, ensure_ascii=False))

    for post in posts:
        posting = post.text
        toneObj= json.dumps(tone_analyzer.tone(tone_input=posting,
                                   content_type="text/plain"), indent=2)
        post.toneObj2 = json.loads(toneObj)
        post.angerScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][0]['score']
        post.disgustScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][1]['score']
        post.fearScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][2]['score']
        post.joyScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][3]['score']
        post.sadScore = post.toneObj2['document_tone']['tone_categories'][0]['tones'][4]['score']

        translation = language_translator.translate(
            text=post.text,
            source='en',
            target='es')
        obj= json.dumps(translation, indent=2, ensure_ascii=False)
        post.obj2 = json.loads(obj)

        post.wordCount = post.obj2['word_count']
        post.letterCount = post.obj2['character_count']
        post.translation = post.obj2['translations'][0]['translation']

        profile = personality_insights.profile(
            content=post.text, content_type='text/plain',
            raw_scores=True, consumption_preferences=True)
        insobj = (json.dumps(profile, indent=2, ensure_ascii=False))
        post.Obj3 = json.loads(insobj)

        post.wordcount = post.Obj3['word_count']
        # post.wordcountmessage = post.Obj3['word_count_message']
        post.percentile = post.Obj3['personality'][0]['percentile']
        post.rawscore = post.Obj3['personality'][0]['raw_score']

        natural = natural_language_understanding.analyze(
            text=post.text,
            features=Features(
                entities=EntitiesOptions(
                    emotion=True,
                    sentiment=True,
                    limit=2),
                keywords=KeywordsOptions(
                    emotion=True,
                    sentiment=True,
                    limit=2)))

        naturalobj = (json.dumps(natural, indent=2))
        post.Obj4 = json.loads(naturalobj)

        post.text1 = post.Obj4['usage']['text_units']
        post.text2 = post.Obj4['usage']['text_characters']
        post.features = post.Obj4['usage']['features']
        post.keywords = post.Obj4['keywords'][0]['text']
        post.negative = post.Obj4['keywords'][0]['sentiment']['score']
        post.sad = post.Obj4['keywords'][0]['emotion']['sadness']
        post.joy = post.Obj4['keywords'][0]['emotion']['joy']
        post.fear = post.Obj4['keywords'][0]['emotion']['fear']
        post.disgust = post.Obj4['keywords'][0]['emotion']['disgust']
        post.anger = post.Obj4['keywords'][0]['emotion']['anger']

    return render(request, 'blog/post_list.html', {'posts': posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Post.objects.get(pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})
