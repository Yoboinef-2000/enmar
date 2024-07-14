from django import template

register = template.Library()

@register.filter
def youtube_embed_url(url):
    if "youtube.com/watch?v=" in url:
        embed_url = url.replace("watch?v=", "embed/")
    elif "youtu.be/" in url:
        embed_url = url.replace("youtu.be/", "youtube.com/embed/")
    else:
        embed_url = url
    return embed_url
