from io import DEFAULT_BUFFER_SIZE
import numpy as np
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, CustomJS, Slider, RadioButtonGroup
from bokeh.embed import components
from bokeh.models import Select
from datetime import date
from bokeh.models import DataTable, TableColumn
import numpy as np
import pandas as pd
from bokeh.models.widgets import HTMLTemplateFormatter


dfData      = pd.read_excel('./definition.xlsx', index_col=None, header=0, sheet_name='def',engine='openpyxl')

methods = dict(
        methodName=dfData['methodName'],
        applicable=dfData['ini'],
    )

srcMethods = ColumnDataSource(methods)
srcDef = ColumnDataSource(dfData)

# use  <%= value %> to access value
template=["""<span style="font-weight: bold; color:<%= 
                (function colorfromint(){
                    if (applicable["""+str(i)+"""] == "x")
                        {return('#85ba22')}
                    else 
                        {return('#ba4d22')}
                    }()) %>;">
                &#x2B24;
            </span>""" for i in range(3)]
template = '\n'.join(template)

formatter =  HTMLTemplateFormatter(template=template)
cols = [
        TableColumn(field="methodName", title="Method"),
        TableColumn(field="applicable", title="Applicability",formatter=formatter),
    ]
tab1 = DataTable(source=srcMethods, columns=cols,index_position=None,sizing_mode="stretch_width",selectable=False)

# define sliders for input
sl1            = Slider(title="pH",start=6.0, end=8.5, value=7.2, step=0.1)
sl2            = Slider(title="Temperature",start=12.0, end=24.0, value=17.3, step=0.1)
sl3            = Slider(title="Hydraulic Conductivity (log10)",start=-9, end=-2, value=-4, step=0.1)

#  define radio button group for shape selections
rG1  = RadioButtonGroup(labels=["aerobic","anaerobic"], active=0)
rG2  = RadioButtonGroup(labels=["accessible","restricted","no access"], active=0)
rG3  = RadioButtonGroup(labels=["saturated","unsaturated"], active=0)
rG4  = RadioButtonGroup(labels=["plume","residual","pool","sorbed"], active=0)
rG5  = RadioButtonGroup(labels=["fractured","alluvial/porous"], active=0)

se1 = Select(title='Contaminant Type',value ='PAH',options=["halogenated","non-halogenated","PAH","PFAS","PCBs","Cationic Trace Elements","Oxyanionic Trace Elements","Pesticides/Herbicides","Complex Cyanides","Asbestos","Energetic Materials","other"])

# callback
with open('myCB.js','r') as file:
    cbCode = file.read()
myCB = CustomJS(args=dict( srcMethods=srcMethods,sl2=sl2,sl1=sl1,rG1=rG1,srcDef=srcDef),code=cbCode)

sl2.js_on_change('value',myCB)
sl1.js_on_change('value',myCB)
rG1.js_on_click(myCB)

# define the layout
layout = column(rG2,sl2,sl1,se1,rG4,sl3,rG1,rG3,rG5,sizing_mode="stretch_width")

# print the script to file
script, (div1,div2) = components((layout,tab1))


# read in the template file
with open('template', 'r') as file :
  filedata = file.read()

# replace the target strings
filedata = filedata.replace('+LEFT+', div1)
filedata = filedata.replace('+SCRIPT+', script)
filedata = filedata.replace('+RIGHT+', div2)
filedata = filedata.replace('+DATE+',date.today().strftime("%Y-%m-%d"))

# write to html file
with open('index.html', 'w') as file:
  file.write(filedata)