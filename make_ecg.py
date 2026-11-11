import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
plt.rcParams['font.family']='DejaVu Sans'
g=lambda t,m,s,a: a*np.exp(-((t-m)**2)/(2*s**2))
def grid(ax,x0,x1,y0,y1):
    ax.set_xticks(np.arange(x0,x1+1e-9,0.2)); ax.set_yticks(np.arange(y0,y1+1e-9,0.5))
    ax.set_xticks(np.arange(x0,x1+1e-9,0.04),minor=True); ax.set_yticks(np.arange(y0,y1+1e-9,0.1),minor=True)
    ax.grid(which='major',color='#e89a9a',lw=0.8); ax.grid(which='minor',color='#f6d5d5',lw=0.4)
    ax.set_xlim(x0,x1); ax.set_ylim(y0,y1); ax.tick_params(labelbottom=False,labelleft=False,length=0,which='both')
    for s in ax.spines.values(): s.set_color('#e89a9a')
def beat(t,o=0):
    return (g(t,o+0.20,0.025,0.15)+g(t,o+0.375,0.008,-0.12)+g(t,o+0.40,0.010,1.2)
            +g(t,o+0.43,0.009,-0.25)+g(t,o+0.66,0.045,0.32))
# 1. normal ECG
t=np.linspace(0,1.0,4000); y=beat(t)
fig,ax=plt.subplots(figsize=(6.5,3.9),dpi=150); grid(ax,0,1.0,-0.9,1.6)
ax.plot(t,y,color='black',lw=1.8)
lab=dict(ha='center',fontsize=13,fontweight='bold',color='#1f3a8a')
ax.text(0.20,0.24,'P',**lab); ax.text(0.362,-0.27,'Q',**lab); ax.text(0.40,1.27,'R',**lab)
ax.text(0.447,-0.40,'S',**lab); ax.text(0.66,0.41,'T',**lab)
def span(a,b,yy,txt,dy=-0.11):
    ax.annotate('',xy=(a,yy),xytext=(b,yy),arrowprops=dict(arrowstyle='<->',color='#b00020',lw=1.2))
    ax.text((a+b)/2,yy+dy,txt,ha='center',fontsize=9,color='#b00020')
span(0.14,0.365,-0.50,'интервал P–Q'); span(0.365,0.455,0.80,'QRS',dy=0.05)
span(0.455,0.56,-0.50,'сегмент S–T'); span(0.365,0.78,-0.74,'интервал Q–T')
ax.text(0.03,0.05,'изолиния',fontsize=8,color='#555')
ax.set_title('Нормальная ЭКГ (один сердечный цикл)',fontsize=12)
fig.tight_layout(); fig.savefig('img/ecg_norma.png'); plt.close(fig)
# 2. rhythm strip
t=np.linspace(0,3.2,9000); y=sum(beat(t,o) for o in (0,0.8,1.6,2.4))
fig,ax=plt.subplots(figsize=(6.5,2.2),dpi=150); grid(ax,0,3.2,-0.6,1.5)
ax.plot(t,y,color='black',lw=1.4)
ax.annotate('',xy=(0.40,1.35),xytext=(1.20,1.35),arrowprops=dict(arrowstyle='<->',color='#b00020',lw=1.2))
ax.text(0.80,1.38,'R–R',ha='center',fontsize=9,color='#b00020')
ax.set_title('Нормальный синусовый ритм: одинаковые расстояния R–R, перед каждым QRS есть зубец P',fontsize=9)
fig.tight_layout(); fig.savefig('img/ecg_ritm.png'); plt.close(fig)
# 3. cat's back
t=np.linspace(0,1.0,4000)
y=g(t,0.20,0.025,0.15)+g(t,0.375,0.008,-0.10)+g(t,0.40,0.010,1.0)
dome=np.where(t>0.415,0.75*np.exp(-((t-0.50)**2)/(2*0.085**2))*(1/(1+np.exp(-(t-0.42)/0.004))),0)
dome=np.where(t>0.50,0.75*np.exp(-((t-0.50)**2)/(2*0.10**2)),dome)
y=np.maximum(y,0)*(t<0.41)+np.where(t<0.41,np.minimum(y,0),0)+np.where(t>=0.41,np.maximum(g(t,0.40,0.010,1.0),dome),0)
fig,ax=plt.subplots(figsize=(6.5,3.4),dpi=150); grid(ax,0,1.0,-0.6,1.4)
ax.plot(t,y,color='black',lw=1.8)
ax.text(0.20,0.24,'P',**lab); ax.text(0.385,1.07,'R',**lab)
ax.annotate('подъём сегмента S–T\n(«кошачья спинка»)',xy=(0.52,0.76),xytext=(0.68,1.05),fontsize=10,color='#b00020',
            arrowprops=dict(arrowstyle='->',color='#b00020'))
ax.axhline(0,color='#555',lw=0.6,ls='--'); ax.text(0.86,0.04,'изолиния',fontsize=8,color='#555')
ax.set_title('ЭКГ при остром инфаркте миокарда: «кошачья спинка»',fontsize=12)
fig.tight_layout(); fig.savefig('img/ecg_infarkt.png'); plt.close(fig)
# 4. electrodes
fig,axs=plt.subplots(1,2,figsize=(6.5,4.2),dpi=150)
ax=axs[0]; ax.set_xlim(-4.6,4.6); ax.set_ylim(-5.2,3.6); ax.axis('off'); ax.set_aspect('equal')
ax.add_patch(plt.Circle((0,2.4),0.6,fc='#f3e3d3',ec='#555'))
ax.add_patch(plt.Rectangle((-0.9,-1.2),1.8,2.9,fc='#f3e3d3',ec='#555'))
for x0,x1 in ((-0.9,-2.0),(0.9,2.0)): ax.plot([x0,x1],[1.5,-1.0],color='#555',lw=7,solid_capstyle='round')
for x in (-0.5,0.5): ax.plot([x,x*1.4],[-1.2,-4.3],color='#555',lw=8,solid_capstyle='round')
pts=[(-2.0,-1.0,'#d62728','Красный\nправая рука',(-4.5,-1.0)),(2.0,-1.0,'#f2c200','Жёлтый\nлевая рука',(2.5,-1.0)),
     (0.7,-4.3,'#2ca02c','Зелёный\nлевая нога',(1.3,-4.3)),(-0.7,-4.3,'black','Чёрный\nправая нога',(-3.6,-4.3))]
for x,y_,c,tx,p in pts:
    ax.add_patch(plt.Circle((x,y_),0.28,fc=c,ec='black',zorder=5)); ax.text(p[0],p[1],tx,fontsize=8,va='center')
ax.annotate('',xy=(2.0,-0.5),xytext=(-2.0,-0.5),arrowprops=dict(arrowstyle='->',color='#1f3a8a',lw=1,connectionstyle='arc3,rad=-0.5'))
ax.text(0,3.3,'по часовой стрелке (смотрим на пациента)',ha='center',fontsize=7,color='#1f3a8a')
ax.set_title('Электроды на конечности',fontsize=10)
ax=axs[1]; ax.set_xlim(-3,3.4); ax.set_ylim(-3.2,3.2); ax.axis('off'); ax.set_aspect('equal')
ax.add_patch(plt.Polygon([(-2.6,2.6),(2.6,2.6),(2.9,-2.8),(-2.9,-2.8)],fc='#f3e3d3',ec='#555'))
ax.add_patch(plt.Rectangle((-0.25,-1.6),0.5,3.9,fc='#e2cdb6',ec='#888'))
ax.text(0,2.35,'грудина',ha='center',fontsize=7,color='#555')
for i,yy in enumerate((1.6,0.9,0.2,-0.5,-1.2)):
    for sgn in (-1,1): ax.plot([sgn*0.25,sgn*2.5],[yy,yy-0.35],color='#b89b7b',lw=5,solid_capstyle='round')
ax.plot([1.45,1.45],[2.5,-2.7],color='#1f3a8a',lw=0.7,ls='--'); ax.text(1.45,-3.05,'среднеключичная\nлиния',ha='center',fontsize=6,color='#1f3a8a')
V=[(-0.55,0.0,'#d62728','V1'),(0.55,0.0,'#f2c200','V2'),(1.0,-0.4,'#2ca02c','V3'),(1.45,-0.8,'#8b4513','V4'),(2.15,-0.8,'black','V5'),(2.8,-0.8,'#7b2fbe','V6')]
for x,y_,c,n in V:
    ax.add_patch(plt.Circle((x,y_),0.2,fc=c,ec='black',zorder=5)); ax.text(x,y_+0.32,n,ha='center',fontsize=8,fontweight='bold')
ax.text(-2.2,2.9,'правая сторона',fontsize=7); ax.text(1.0,2.9,'левая сторона',fontsize=7)
ax.set_title('Грудные электроды V1–V6 (схема)',fontsize=10)
fig.tight_layout(); fig.savefig('img/ecg_elektrody.png'); plt.close(fig)
