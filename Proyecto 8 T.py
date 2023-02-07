#!/usr/bin/env python
# coding: utf-8

# # ¡Hola, Juan!  
# 
# Mi nombre es Carlos Ortiz, soy code reviewer de Practicum y voy a revisar el proyecto que acabas de desarrollar.
# 
# Cuando vea un error la primera vez, lo señalaré. Deberás encontrarlo y arreglarlo. La intención es que te prepares para un espacio real de trabajo. En un trabajo, el líder de tu equipo hará lo mismo. Si no puedes solucionar el error, te daré más información en la próxima ocasión. 
# 
# Encontrarás mis comentarios más abajo - **por favor, no los muevas, no los modifiques ni los borres**.
# 
# ¿Cómo lo voy a hacer? Voy a leer detenidamente cada una de las implementaciones que has llevado a cabo para cumplir con lo solicitado. Verás los comentarios de esta forma:
# 
# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Si todo está perfecto.
# </div>
# 
# 
# <div class="alert alert-block alert-warning">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Si tu código está bien pero se puede mejorar o hay algún detalle que le hace falta.
# </div>
# 
# 
# <div class="alert alert-block alert-danger">
#     
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
#     
# Si de pronto hace falta algo o existe algún problema con tu código o conclusiones.
# </div>
# 
# 
# Puedes responderme de esta forma: 
# 
# 
# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>
# 
# ¡Empecemos!

# ## Descripción del proyecto
# Eres analista en una gran tienda en línea. Junto con el departamento de marketing has recopilado una lista de hipótesis que pueden ayudar a aumentar los ingresos. Revisaremos y priorizaremos las hipótesis luego aplicaremos un test A/B para determinar cual grupo nos entrega mejores resultados.

# ## Objetivo:  
# Priorizar las hipótesis, lanzar un test A/B y analizar los resultados.
# 
# ## Etapas 
#  
# El proyecto consistirá en dos etapas:
#  1. Descripción de los datos
#  2. Priorizar hipótesis
#  3. Análisis de test A/B

# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# In[1]:


import pandas as pd
import seaborn as sns
import numpy as np
from scipy import stats as st
import math as mth
import datetime as dt
import matplotlib.pyplot as plt
import scipy.stats as stats


# In[2]:


hypo   = pd.read_csv('/datasets/hypotheses_us.csv', sep=';')
orders = pd.read_csv('/datasets/orders_us.csv')
visits = pd.read_csv('/datasets/visits_us.csv')


# In[3]:


hypo.head()


# In[4]:


hypo.info()


# In[5]:


orders.head()


# In[6]:


orders.info()


# In[7]:


orders['date'] = orders['date'].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))


# In[8]:


orders.info()


# In[9]:


orders.describe()


# In[10]:


orders.describe(exclude='number')


# In[11]:


orders.group.value_counts()


# In[12]:


orders.visitorId.nunique()


# In[13]:


orders.duplicated().sum()


# In[14]:


visits.head()


# In[15]:


visits['date'] = visits['date'].map(lambda x: dt.datetime.strptime(x, '%Y-%m-%d'))


# In[16]:


visits.info()


# In[17]:


visits.describe()


# In[18]:


visits.describe(exclude='number')


# In[19]:


visits.duplicated().sum()


# ## Conclusión descripción de los datos
# Tras analizar la información general corregimos formatos de fecha, encontramos datos atípicos que serán materia de investigación, no encontramos nulos ni duplicados aparentes. Finalmente sabemos que el periodo de prueba esta entre el 01-08-2019 y el 31-08-2019.

# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Buen trabajo con esta exploración inicial.
# </div>

# ## Priorizar hipótesis

# In[20]:


hypo


# In[21]:


# Metodo ICE
hypo['ICE'] = (hypo['Impact'] * hypo['Confidence']) / hypo['Effort']

print(hypo[['Hypothesis','ICE']].sort_values(by='ICE', ascending=False))


# In[22]:


# Metodo RICE
hypo['RICE'] = (hypo['Reach'] *  hypo['Impact'] * hypo['Confidence']) / hypo['Effort']

print(hypo[['Hypothesis','RICE']].sort_values(by='RICE', ascending=False))


# In[23]:


hypo


# In[24]:


#plt.scatter(hypo['ICE'], hypo['RICE']);
sns.displot(data=hypo, x='ICE',y='RICE',hue='Hypothesis');


# ## Conclusión
# Tras comparar el método ICE y RICE vemos que la hipótesis (Añadir un formulario de suscripción a todas las páginas principales) se posiciono en primer lugar en el método RICE, esto se debe a que RICE incorpora el parámetro alcance (cuántos usuarios se verán afectados) el cual según la escala de clasificación a la cual esta sometida le otorga un 10 dándole una prioridad máxima a este punto. Tras analizar el gráfico de dispersión, vemos que existe correlación entre RICE y ICE para posicionar a la hipótesis gris y verde como las mas prioritarias.

# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# ## Análisis de test A/B

# In[25]:


# Revisamos el grupo a
df_a = orders[orders['group'] == 'A'].reset_index()
df_a


# In[26]:


# Revisamos el grupo b
df_b = orders[orders['group'] == 'B'].reset_index()
df_b


# In[27]:


# vemos quienes son los usuarios de a en b
df_ab = df_a[df_a['visitorId'].isin(df_b['visitorId'])].reset_index()
df_ab


# In[28]:


# Filtramos la tabla para eliminar los usuarios
filtered = orders[~orders['visitorId'].isin(df_ab['visitorId'])].reset_index(drop=True)
filtered


# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# Representa gráficamente el ingreso acumulado por grupo. Haz conclusiones y conjeturas.

# In[29]:


# Matriz con valores únicos de parejas fecha-grupo
datesGroups = filtered[['date','group']].drop_duplicates()
datesGroups


# In[30]:


# Obténemos los datos diarios acumulados agregados sobre los pedidos
ordersAggregated = datesGroups.apply(lambda x: filtered[np.logical_and(filtered['date'] <= x['date'],
filtered['group'] == x['group'])].agg({'date' : 'max', 'group' : 'max', 'transactionId' : pd.Series.nunique, 'visitorId' : pd.Series.nunique, 'revenue' : 'sum'}),
axis=1).sort_values(by=['date','group'])
ordersAggregated.head()


# In[31]:


# Obténemos los datos diarios acumulados agregados sobre los visitantes
visitorsAggregated = datesGroups.apply(lambda x: visits[np.logical_and(visits['date'] <= x['date'],
visits['group'] == x['group'])].agg({'date' : 'max', 'group' : 'max', 'visits' : 'sum'}),
axis=1).sort_values(by=['date','group'])
visitorsAggregated.head()


# In[32]:


# fusionamos las dos tablas en una y da a sus columnas nombres descriptivos
cumulativeData = ordersAggregated.merge(visitorsAggregated, left_on=['date', 'group'], right_on=['date', 'group'])
cumulativeData.columns = ['date', 'group', 'orders', 'buyers', 'revenue', 'visitors']

print(cumulativeData.head(5))


# In[33]:


# DataFrame con pedidos acumulados e ingresos acumulados por día, grupo A
cumulativeRevenueA = cumulativeData[cumulativeData['group']=='A'][['date','revenue', 'orders']]
cumulativeRevenueA.head()


# In[34]:


cumulativeRevenueB = cumulativeData[cumulativeData['group']=='B'][['date','revenue', 'orders']]
cumulativeRevenueB.head()


# In[35]:


# Trazamos el gráfico de ingresos del grupo A
plt.figure(figsize=(14, 5))
plt.plot(cumulativeRevenueA['date'], cumulativeRevenueA['revenue'], label='A')
# Trazar el gráfico de ingresos del grupo B
plt.plot(cumulativeRevenueB['date'], cumulativeRevenueB['revenue'], label='B')
plt.title('Gráfico comparativo entre A/B')
plt.ylabel('Ingresos')
plt.xlabel('Días')
plt.legend();


# ## Conclsión ingreso acumulado por grupo
# Tras análizar el primer gráfico nos muestra que los ingresos aumentan constantemente, el grupo B muestra un alza significativa a partir del día 18 de agosto.

# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Buen trabajo.
# </div>

# Representa gráficamente el tamaño de pedido promedio acumulado por grupo. Haz conclusiones y conjeturas.

# In[36]:


# Vamos a trazar el tamaño promedio de compra por grupo. Vamos a dividir los ingresos acumulados entre el número acumulado de pedidos:
plt.figure(figsize=(14, 5))
plt.plot(cumulativeRevenueA['date'], cumulativeRevenueA['revenue']/cumulativeRevenueA['orders'], label='A')
plt.plot(cumulativeRevenueB['date'], cumulativeRevenueB['revenue']/cumulativeRevenueB['orders'], label='B')
plt.title('Gráfico comparativo entre A/B')
plt.ylabel('Compras')
plt.xlabel('Días')
plt.legend();


# ## Conclusión tamaño promedio acumulado
# El tamaño promedio de compra tiende a estabilizarce al final del periodo de prueba, Tambien el grupo B muestra un alza significativa en su tamaño desde el día 18 de agosto. 

# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Buen trabajo y coincido con tus conclusiones.
#     
# </div>

# Representa gráficamente la diferencia relativa en el tamaño de pedido promedio acumulado para el grupo B en comparación con el grupo A. Haz conclusiones y conjeturas.

# In[37]:


# reunimos los datos en un DataFrame
mergedCumulativeRevenue = cumulativeRevenueA.merge(cumulativeRevenueB, left_on='date', right_on='date', how='left', suffixes=['A', 'B'])
mergedCumulativeRevenue.head()


# In[38]:


# trazamos un gráfico de diferencia relativa para los tamaños de compra promedio
plt.figure(figsize=(14, 5))
plt.plot(mergedCumulativeRevenue['date'], (mergedCumulativeRevenue['revenueB']/mergedCumulativeRevenue['ordersB'])/(mergedCumulativeRevenue['revenueA']/mergedCumulativeRevenue['ordersA'])-1)
plt.title('Diferencia relativa para los tamaños de compra promedio')
plt.ylabel('Tasas')
plt.xlabel('Días')
plt.legend('Tendencia')
# agregar el eje X
plt.axhline(y=0, color='black', linestyle='--');


# ## Conclusión diferencia relativa en el tamaño de pedido promedio acumulado
# En varios puntos, la diferencia entre los segmentos aumenta. Esto significa que deben haber algunos pedidos grandes y valores atípicos.

# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
# 
# Buen trabajo. Habrá que analizarlo más adelante.
# </div>

# Calcula la tasa de conversión de cada grupo como la relación entre los pedidos y el número de visitas de cada día. Representa gráficamente las tasas de conversión diarias de los dos grupos y describe la diferencia. Saca conclusiones y haz conjeturas.

# In[39]:


# calculo de la conversión acumulada
cumulativeData['conversion'] = cumulativeData['orders']/cumulativeData['visitors']
cumulativeData.head()


# In[40]:


# seleccionamos datos en el grupo A
cumulativeDataA = cumulativeData[cumulativeData['group']=='A']
cumulativeDataA.head()


# In[41]:


# seleccionamos datos en el grupo B
cumulativeDataB = cumulativeData[cumulativeData['group']=='B']
cumulativeDataB.head()


# In[42]:


# trazamos los gráficos
plt.figure(figsize=(14, 5))
plt.plot(cumulativeDataA['date'], cumulativeDataA['conversion'], label='A')
plt.plot(cumulativeDataB['date'], cumulativeDataB['conversion'], label='B')
plt.title('Gráfico de tasa de conversión diaria')
plt.ylabel('Tasas')
plt.xlabel('Días')
plt.legend();


# ## Conclusión tasa de conversión diaria
# Tanto el grupo B como el grupo A tienden a estabilizar su tasa de conversión al final de la muestra. ambos grupos fluctuaron en valores distintos, El grupo B una vez se estabilizó empezó a mostrar mejores números que A.

# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# In[43]:


# Vamos a trazar un gráfico de diferencia relativa para las tasas de conversión acumuladas:
mergedCumulativeConversions = cumulativeDataA[['date','conversion']].merge(cumulativeDataB[['date','conversion']], left_on='date', right_on='date', how='left', suffixes=['A', 'B'])
mergedCumulativeConversions.head()


# In[44]:


plt.figure(figsize=(14, 5))
plt.plot(mergedCumulativeConversions['date'], mergedCumulativeConversions['conversionB']/mergedCumulativeConversions['conversionA']-1)
plt.legend('Tendencia')
plt.title('Diferencia relativa para las tasas de conversión acumuladas')
plt.ylabel('Tasas')
plt.xlabel('Días')
plt.axhline(y=0, color='black', linestyle='--')
plt.axhline(y=-0.1, color='grey', linestyle='--');


# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# ## Conclusión diferencia relativa para las tasas de conversión acumulada
# Al trazar un gráfico de diferencia relativa para las tasas de conversión acumulada vemos que B inica por debajo de A pero luego tiene un alza a partir del 7 de agosto y luego se estabiliza al final del periodo.

# Traza un gráfico de dispersión del número de pedidos por usuario. Haz conclusiones y conjeturas.

# In[45]:


# Vamos a buscar el número de pedidos por usuario e imprimir el resultado:
ordersByUsers = (
    filtered.drop(['group', 'revenue', 'date'], axis=1)
    .groupby('visitorId', as_index=False)
    .agg({'transactionId': pd.Series.nunique})
)
ordersByUsers.columns = ['userId', 'orders']

print(ordersByUsers.sort_values(by='orders', ascending=False).head(10))


# In[46]:


# Vamos a trazar un gráfico de dispersión con el número de pedidos por usuario:
x_values = pd.Series(range(0,len(ordersByUsers)))

plt.scatter(x_values, ordersByUsers['orders']);


# ## Conclusión dispersión del número de pedidos
# Como muestra el gráfico de dispersión la mayoria de los clientes realizó un pedido, varios realizaron 2 pedidos y 7 usuarios realizaron 3 pedidos.

# Calcula los percentiles 95 y 99 para el número de pedidos por usuario. Define el punto en el cual un punto de datos se convierte en una anomalía.

# In[47]:


print(np.percentile(ordersByUsers['orders'], [95, 99]))


# No mas del 5% de los usuarios realizaron 1 pedido y no mas del 1% realizó 2 pedidos.Por lo tanto, sería razonable establecer tres pedidos por usuario como límite inferior para el número de pedidos y filtrar las anomalías en base a ello.

# Traza un gráfico de dispersión de los precios de los pedidos. Haz conclusiones y conjeturas.

# In[48]:


x_values = pd.Series(range(0, len(filtered['revenue'])))
plt.scatter(x_values, filtered['revenue']);


# Calcula los percentiles 95 y 99 de los precios de los pedidos. Define el punto en el cual un punto de datos se convierte en una anomalía.

# In[49]:


print(np.percentile(filtered['revenue'], [95, 99]))


# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Buen trabajo en esta sección.
# </div>

# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# ## Conclusión dispersión de ingresos por ususario
# Según muestra el gráfico de conversión no mas del 5% de los ingresos son por 414. y no mas del 1 % cuesta 830.
# Establecemos el ingreso de $2500 como base limite.

# Encuentra la significancia estadística de la diferencia en la conversión entre los grupos utilizando los datos en bruto. Haz conclusiones y conjeturas.

# In[50]:


# Calculamos la significancia estadística de la diferencia de conversión entre los grupos.
ordersByUsersA = filtered[filtered['group']=='A'].groupby('visitorId', as_index=False).agg({'transactionId' : pd.Series.nunique})
ordersByUsersA.columns = ['userId', 'orders']
ordersByUsersA.head()


# In[51]:


ordersByUsersB = filtered[filtered['group']=='B'].groupby('visitorId', as_index=False).agg({'transactionId' : pd.Series.nunique})
ordersByUsersB.columns = ['userId', 'orders'] 
ordersByUsersB.head()


# In[52]:


sampleA = pd.concat([ordersByUsersA['orders'],pd.Series(0, index=np.arange(visits[visits['group']=='A']['visits'].sum() - len(ordersByUsersA['orders'])), name='orders')],axis=0)

sampleB = pd.concat([ordersByUsersB['orders'],pd.Series(0, index=np.arange(visits[visits['group']=='B']['visits'].sum() - len(ordersByUsersB['orders'])), name='orders')],axis=0)

print("{0:.3f}".format(stats.mannwhitneyu(sampleA, sampleB)[1]))

print("{0:.3f}".format(sampleB.mean()/sampleA.mean()-1)) 


# ## Conclusión significancia estadística de la diferencia en la conversión
# La primera fila de la salida nos da el valor p 0.011, que es menor que 0,05. Entonces, rechazamos la hipótesis nula ya que si hay una diferencia estadísticamente significativa en la conversión entre los grupos. Pero la pérdida relativa del grupo B es del 16%.

# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido. 
# </div>

# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Me estas diciendo que el valor de p 0.011 es mas bajo que 0.05 ??. 
# </div>

# Encuentra la significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos en bruto. Haz conclusiones y conjeturas.

# In[54]:


# Encontramos la diferencia relativa en el tamaño promedio de pedido entre los grupos:
print('{0:.3f}'.format(stats.mannwhitneyu(filtered[filtered['group']=='A']['revenue'], filtered[filtered['group']=='B']['revenue'])[1]))
print('{0:.3f}'.format(filtered[filtered['group']=='B']['revenue'].mean()/filtered[filtered['group']=='A']['revenue'].mean()-1)) 


# ## Conclusión significancia estadística de la diferencia en el tamaño promedio de pedido
# El valor p es notablemente superior a 0,05 por lo que no hay motivo para rechazar la hipótesis nula y concluir que el tamaño medio de los pedidos difiere entre los grupos. No obstante, el tamaño de pedido promedio para el grupo B es mucho más pequeño que para el grupo A.

# <div class="alert alert-block alert-success">
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Buen trabajo en esta sección.
# </div>

# In[55]:


usersWithManyOrders = pd.concat([ordersByUsersA[ordersByUsersA['orders'] > 2]['userId'], ordersByUsersB[ordersByUsersB['orders'] > 2]['userId']], axis = 0)
usersWithExpensiveOrders = filtered[filtered['revenue'] > 830]['visitorId']
abnormalUsers = pd.concat([usersWithManyOrders, usersWithExpensiveOrders], axis = 0).drop_duplicates().sort_values()
print(abnormalUsers.head(5))
print(abnormalUsers.shape)


# <div class="alert alert-block alert-info">
# <b>Respuesta del estudiante</b> <a class="tocSkip"></a>
#     
# Corregido
# </div>

# ## Conclusión
# Encontramos la presencia de 19 usuarios anómalos según nuestro criterio de 2 pedidos y sobre 830.

# Encuentra la significancia estadística de la diferencia en la conversión entre los grupos utilizando los datos filtrados. Haz conclusiones y conjeturas.

# In[56]:


sampleAFiltered = pd.concat([ordersByUsersA[np.logical_not(ordersByUsersA['userId'].isin(abnormalUsers))]['orders'],
                             pd.Series(0,
                                       index=np.arange(visits[visits['group']=='A']['visits'].sum() - len(ordersByUsersA['orders'])),
                                       name='orders')]
                            ,axis=0)

sampleBFiltered = pd.concat([ordersByUsersB[np.logical_not(ordersByUsersB['userId'].isin(abnormalUsers))]['orders'],pd.Series(0, index=np.arange(visits[visits['group']=='B']['visits'].sum() - len(ordersByUsersB['orders'])),name='orders')],axis=0)


# In[57]:


print("{0:.3f}".format(stats.mannwhitneyu(sampleAFiltered, sampleBFiltered)[1]))
print("{0:.3f}".format(sampleBFiltered.mean()/sampleAFiltered.mean()-1)) 


# ## Conclusión
# Tras aplicar el criterio estadístico de Mann-Whitney a nuestra tabla filtrada, concluimos que el valor de p disminuyó quedando por debajo de nuestro nivel de significancia por ende debemos rechazar la hipótesis ya que hay una diferencia estadísticamente significativa en la conversión entre los grupos. La perdida relativa pasó de 16% a 19%.

# Encuentra la significancia estadística de la diferencia en el tamaño promedio de pedido entre los grupos utilizando los datos filtrados. Haz conclusiones y conjeturas.

# In[58]:


print('{0:.3f}'.format(stats.mannwhitneyu(
    filtered[np.logical_and(
        filtered['group']=='A',
        np.logical_not(filtered['visitorId'].isin(abnormalUsers)))]['revenue'],
    filtered[np.logical_and(
        filtered['group']=='B',
        np.logical_not(filtered['visitorId'].isin(abnormalUsers)))]['revenue'])[1]))

print('{0:.3f}'.format(
    filtered[np.logical_and(filtered['group']=='B',np.logical_not(filtered['visitorId'].isin(abnormalUsers)))]['revenue'].mean()/
    filtered[np.logical_and(
        filtered['group']=='A',
        np.logical_not(filtered['visitorId'].isin(abnormalUsers)))]['revenue'].mean() - 1))


# El valor de p aumentó pero ahora la diferencia entre los segmentos es del 1.4% en lugar del 27%.

# Toma una decisión basada en los resultados de la prueba. Las decisiones posibles son: 1. Para la prueba, considera a uno de los grupos como líder. 2. Para la prueba, concluye que no hay diferencia entre los grupos. 3. Continúa la prueba.

# Tras analizar los datos concluimos que:
# * Hay una diferencia estadísticamente significativa en la conversión entre los grupos, según los datos sin procesar y filtrados.
# 
# * Los datos sin procesar no mostraron una diferencia estadísticamente significativa entre los grupos en cuanto a tamaño promedio de compra. Sin embargo, después de eliminar las anomalías, resultó que había una diferencia estadísticamente significativa.
# 
# * El gráfico de la diferencia de conversión entre los grupos muestra que los resultados del grupo B parten por debajo de A pero despues del dia 7 de agosto son mejores que los del grupo A: tienen tendencia a crecer o se estabilizaron alrededor de la media.
# 
# * Finalmente tomamos la decisión 1. Consideramos la prueba exitosamente y el grupo B se alzo como líder de la prueba.

# <div class="alert alert-block alert-danger">
#     
# # Comentarios generales
#     
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Buen trabajo, Juan. Has implementado correctamente gran parte de lo solicitado y cumplido con gran parte de los objetivos del proyecto. Sin embargo, debemos trabajar en algunos puntos que quedaron pendientes o que requieren de mayor atención. He dejado comentarios a lo largo del documento para ello.
#     
# Adicionalmente, debemos trabajar en los gráficos. Estos podrían ser más grandes para poder apreciar mejor los detalles de la información, agrégales un título, un nombre a los ejes y una leyenda. Esto con el fin de que el usuario entienda sin mayor explicación a que se hace referencia con ellos.
#     
# Una vez las correcciones sugeridas sean, implementadas el proyecto será aprobado.
# </div>

# <div class="alert alert-block alert-danger">
#     
# # Comentarios generales #2
#     
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Gran trabajo, Juan. Has corregido casi todo lo indicado. Lo único que nos hace falta es actualizar la conclusión con respecto a la diferencia entre 0.011 y 0.05.
# </div>

# <div class="alert alert-block alert-success">
#     
# # Comentarios generales #3
#     
# <b>Comentario del revisor</b> <a class="tocSkip"></a>
#     
# Perfecto. Todo ha sido corregido y has aprobado un nuevo proyecto.
#     
# ¡Felicitaciones!
# </div>
