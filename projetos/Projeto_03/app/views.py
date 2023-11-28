from django.shortcuts import render, redirect
import pandas as pd
from sqlalchemy import create_engine
from app.forms import ProductsForm

data = {}
# Create your views here.
def home(request):
    con = create_engine('mysql://root:@localhost/recomendacao_projeto03')
    df = pd.read_sql_table('app_products',con)
    # print(df.head())
    idCat,cat = pd.factorize(df['categoria'])
    # print(idCat)
    df['categoriaCat']=idCat
    del df['categoria']
    del df['id']
    # print(df.head())

    newDf = pd.DataFrame({
        'media': df.groupby('product')['ratings'].mean().values,
        'contagem': df.groupby('product')['product'].count().values,
        'categoria':df.groupby('product')['categoriaCat'].max().values
    },index=df.groupby('product')['product'].count().index)

    # Indicação apenas por quantidade de classificações
    # print(newDf[newDf['contagem']>2].sort_values('contagem',ascending=False))
    # data['recomendado'] = newDf[newDf['contagem'] > 2].sort_values('contagem', ascending=False).index

    # Indicação por média e quantidade de classificações
    # print(newDf[newDf['contagem'] > 2].sort_values(['contagem','media'], ascending=[False,False]))

    # Indicação por média e quantidade de classificações e por categoria
    categoriaUser = df[df['user_id']==3]['categoriaCat'].values[0]
    #print(newDf[(newDf['contagem'] > 2) & (newDf['categoria']==categoriaUser)].sort_values(['contagem', 'media'], ascending=[False, False]))
    data['recomendado'] = newDf[(newDf['contagem'] > 2) & (newDf['categoria']==categoriaUser)].sort_values(['contagem', 'media'], ascending=[False, False]).index
    return render(request,'home.html',data)

def form(request):
    data['form']=ProductsForm()
    return render(request, 'form.html',data)

def comentar(request):
    form = ProductsForm(request.POST or None)
    if form.is_valid():
        form.save()
    return redirect('/form')