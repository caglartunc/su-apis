# Adapted from the lab's partners_map script: same layout/colours, but uses the
# Natural Earth 110m file directly (geopandas>=1.0 dropped the bundled dataset),
# removes axis labels, and writes a PNG for the website.
import sys, warnings; warnings.filterwarnings("ignore")
import geopandas as gpd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
shp, out = sys.argv[1], sys.argv[2]
plt.rcParams["font.family"] = "DejaVu Sans"
RED="#8B2332"; GRAY="#3C3C3C"; LAND="#EDE7E3"; EDGE="#FFFFFF"; SEA="#F8F5F3"
w = gpd.read_file(shp)
SU = (29.38, 40.89)
P = [
 ("University of Edinburgh",-3.19,55.95,-23.5,58.9,"left"),
 ("Edinburgh Napier University",-3.21,55.93,-23.5,57.0,"left"),
 ("IBM Research Dublin",-6.40,53.40,-23.5,54.6,"left"),
 ("University of Birmingham",-1.93,52.45,-23.5,52.4,"left"),
 ("Imperial College London",-0.175,51.498,-23.5,50.6,"left"),
 ("CentraleSupélec (Rennes)",-1.62,48.12,-23.5,47.6,"left"),
 ("CTTC (Barcelona)",1.99,41.28,5.5,37.6,"center"),
 ("KUIS AI, Koç University",29.07,41.20,30.3,46.2,"left"),
 ("Oredata",29.01,41.08,30.3,44.6,"left"),
 ("Enerjisa",29.12,40.99,30.3,43.0,"left"),
 ("METU (Ankara)",32.78,39.89,35.0,38.2,"center"),
 ("Bilkent University",32.74,39.87,35.0,36.6,"center"),
]
fig = plt.figure(figsize=(6.2,3.6), facecolor=SEA); ax = fig.add_axes([0,0,1,1])
ax.set_facecolor(SEA); w.plot(ax=ax, color=LAND, edgecolor=EDGE, linewidth=0.6)
ax.set_xlim(-24,40); ax.set_ylim(34.5,60); ax.set_aspect(1.45)
for n,x,y,tx,ty,ha in P:
    ax.add_patch(FancyArrowPatch(SU,(x,y),connectionstyle="arc3,rad=0.18",arrowstyle="-",color=RED,lw=0.9,alpha=0.45,zorder=2))
    ax.scatter(x,y,s=22,color=GRAY,edgecolor="white",lw=0.8,zorder=4)
    ax.annotate(n,(x,y),xytext=(tx,ty),ha=ha,va="center",fontsize=7,color=GRAY,zorder=5,
        arrowprops=dict(arrowstyle="-",color="#9A9A9A",lw=0.5,shrinkA=2,shrinkB=3))
ax.scatter(*SU,s=120,color=RED,edgecolor="white",lw=1.4,zorder=6,marker="*")
ax.text(28.4,38.6,"Sabancı University\nSU-APIS",fontsize=7.8,color=RED,weight="bold",ha="right",va="center",zorder=6)
ia = fig.add_axes([0.09,0.03,0.24,0.32]); ia.set_facecolor(SEA)
w.plot(ax=ia, color=LAND, edgecolor=EDGE, linewidth=0.5)
ia.set_xlim(-95,-70); ia.set_ylim(35,46); ia.set_aspect(1.3)
ia.scatter(-83.03,40.00,s=22,color=GRAY,edgecolor="white",lw=0.8,zorder=4)
ia.text(-83.03,41.6,"The Ohio State Univ.",ha="center",fontsize=6.6,color=GRAY)
ia.scatter(-76.94,38.99,s=22,color=GRAY,edgecolor="white",lw=0.8,zorder=4)
ia.text(-80.5,36.9,"Univ. of Maryland",ha="center",fontsize=6.6,color=GRAY)
ia.scatter(-74.00,40.73,s=22,color=GRAY,edgecolor="white",lw=0.8,zorder=4)
ia.text(-74.00,43.2,"New York Univ.",ha="center",fontsize=6.6,color=GRAY)
ia.text(-94,36.0,"USA",fontsize=7,color="#787878")
for a in (ax, ia):
    a.set_xticks([]); a.set_yticks([]); a.set_xlabel(""); a.set_ylabel("")
for s in ia.spines.values(): s.set_edgecolor("#787878"); s.set_linewidth(0.6)
for s in ax.spines.values(): s.set_visible(False)
fig.savefig(out, dpi=300, facecolor=SEA, bbox_inches="tight", pad_inches=0.02)
print("saved", out)
