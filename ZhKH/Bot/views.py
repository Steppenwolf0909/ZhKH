from .models import News, Proposal

def get_last_news():
    newsArray=''
    news = News.objects.all()[:3]
    for n in news:
        newsArray+=str(n.title) + '\n ' + str(n.text) + '\n' + '*****************************' + '\n'
    print(newsArray)
    return newsArray

def create_proposal(message):
    propos=Proposal.objects.create(description=message)
    return 'Создано обращение под номером %s. В ближайшее время оно будет рассмотрено' % propos.id