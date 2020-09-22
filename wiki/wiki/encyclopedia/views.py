from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
import markdown2
from . import util
import random as rd

class NewTaskForm(forms.Form):
    #encyclopedia = forms.CharField(label="New Task:")
    #comment = forms.CharField(widget=forms.Textarea)
    encyclopedia=forms.CharField(label="Title",widget=forms.TextInput(attrs={'placeholder':'Title of Document','autofocus':True,'class':'form-control','id':'title'}))
    comment=forms.CharField(label="Content",widget=forms.Textarea(attrs={'class':'form-control'}))


def index(request):
    if 'encyclopedias' not in request.session:
        request.session['encyclopedias'] =[]
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        'encyclopedias': request.session['encyclopedias']
    })



"""def view(request,title):
    html=util.get_entry(title.capitalize())
    if util.get_entry(title) is None:
        return render(request,'encyclopedia/404.html')
    return render ( request ,"encyclopedia/page.html" , {
        'entries' : markdown2.markdown(html),#html,safe_mode='remove').
        'title': title
    })"""

def create(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task= form.cleaned_data['encyclopedia']
            area=form.cleaned_data['comment']
            if task in util.list_entries():
                return render (request, 'encyclopedia/404.html')
            #request.session['encyclopedias'] += [task]
            else :
                util.save_entry(task,area)
            return HttpResponseRedirect(reverse('encyclopedia:index'))
        else:
            return render (request, 'encyclopedia/create.html', {'form':form})
    return render(request,'encyclopedia/create.html', {'form': NewTaskForm()})



def entry_page(request,title):
    if len(title.split("."))==1:
        title=title+".md"
    t,e=title.split(".")
    if util.get_entry(t.lower().capitalize()) is None:
        return render (request,'encyclopedia/NotFound.html')
    else:
        t=t.capitalize()
        html=util.get_entry(t.lower().capitalize())
        mder= markdown2.markdown(html,safe_mode='remove')
        return render( request,"encyclopedia/entry.html", {
            'content':mder,
            "title":t,
            "form":NewTaskForm(),
        })

def editpage(request,title):
    html=util.get_entry(title.lower().capitalize())
    if request.method== 'GET':
        formulario = NewTaskForm(request.POST)
        if title in util.list_entries():
            util.list_entries().remove(title)
            """if html!= formulario.comment:        
                html=formulario
                util.save_entry(title,html)
                return HttpResponse("diferentes")"""
                    #return HttpResponseRedirect(reverse('encyclopedia:index'))
        formulario = NewTaskForm(initial={ 'encyclopedia':"HOLA", 'comment':"SA" })
        formulario.initial
        return render(request,'encyclopedia/edit.html', {'form': formulario})
    return HttpResponseRedirect(reverse('encyclopedia:index'))

def search(request):
    title  = request.GET['q']
    if title in util.list_entries():
        if util.get_entry(title):
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))
        else:
            # query does not match!
            return render(request, "encyclopedia/index.html", {
                "entries": [entry for entry in util.list_entries() if title.lower() in entry.lower()],
                "title": f'"{title}" search results',
                "heading": f'Search Results for "{title}"'
        })
    return render(request,"encyclopedia/NotFound.html")


def random_page(request):
    entry= rd.choice(util.list_entries())
    return HttpResponseRedirect(reverse('encyclopedia:entry',args=(entry,)))