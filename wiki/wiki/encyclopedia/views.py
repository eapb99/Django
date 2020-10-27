from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render,redirect
from django.urls import reverse
import markdown2
from . import util
import random as rd

class NewTaskForm(forms.Form):
    encyclopedia=forms.CharField(label="Title",widget=forms.TextInput(attrs={'placeholder':'Title of Document','autofocus':True,'class':'form-control','id':'title'}))
    comment=forms.CharField(label="Content",widget=forms.Textarea(attrs={'class':'form-control'}))
    edit = forms.BooleanField(initial=False, widget=forms.HiddenInput(), required=False)

def index(request):
    if 'encyclopedias' not in request.session:
        request.session['encyclopedias'] =[]
    return render(request, "encyclopedia/index.html", {
        "entries":[e for e in  util.list_entries() ],
        'encyclopedias': request.session['encyclopedias']
    })

def create(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task= form.cleaned_data['encyclopedia']
            area=form.cleaned_data['comment']
            task=task.lower().capitalize()
            l=[]
            for i in util.list_entries():
                l.append(i.lower().capitalize())
            if task in l:
                mensaje ="""This entry does exist in the encyclopedia.
                                Please change the title."""
                return render (request, 'encyclopedia/create.html',{"mensaje":mensaje,"form":form,"type":"Add Task"})
            else :
                util.save_entry(task,area)
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(task,)))
        else:
            return render (request, 'encyclopedia/create.html', {'form':form,"type":"Add Task"})
    return render(request,'encyclopedia/create.html', {'form': NewTaskForm(),"type":"Add Task"})

def entry_page(request,title):
    if len(title.split("."))==1:
        title=title+".md"
    t,e=title.split(".")
    if util.get_entry(t) is None:
        return render (request,'encyclopedia/NotFound.html', {'title':t.upper()})
    else:
        html=util.get_entry(t)
        mder= markdown2.markdown(html)
        return render( request,"encyclopedia/entry.html", {
            'content':mder,
            "title":t.lower().capitalize(),
            "form":NewTaskForm(),
        })

def editpage(request,title):
    content = util.get_entry(title)
    if content is None:
        return render(request,'encyclopedia/NotFound.html', {'title': title})
    else: 
        form = NewTaskForm()
        form.fields['encyclopedia'].initial=title
        form.fields["comment"].initial= content
        form.fields["edit"].initial=True
        return render(request,'encyclopedia/edit.html', {'form': form,'title':title})

def submit(request):
    if request.method == 'POST':
        form = NewTaskForm(request.POST)
        if form.is_valid():
            task= form.cleaned_data['encyclopedia']
            area=form.cleaned_data['comment']
            task=task.lower().capitalize()
            area=area.split("\n")
            for line in area:
                if line==("\r"):
                    line=""
            area="".join(area)
            util.save_entry(task,area)
        return HttpResponseRedirect(reverse("encyclopedia:entry", args=(task,)))

def search(request):
    title  = request.GET['q']
    L = [entry for entry in util.list_entries() if title.lower() in entry.lower()]
    if len(L)!=0:
        if util.get_entry(title):
            return HttpResponseRedirect(reverse("encyclopedia:entry", args=(title,)))
        else:
            return render(request, "encyclopedia/search.html", {
                "entries": L,
                "title": f'"{title}" search results',
                "heading": f'All results that contain "{title}"'
        })
    return render(request,"encyclopedia/NotFound.html", {'title':title.upper()})


def random_page(request):
    entry= rd.choice(util.list_entries())
    return HttpResponseRedirect(reverse('encyclopedia:entry',args=(entry,)))