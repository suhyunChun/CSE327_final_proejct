import numpy as np
import pickle
import tools.visualization as vis
from datetime import datetime
from analysis.compare_gt import align_gt
from reconstruction import synchronization as sync
import simplekml
from kalman import iterate


data=0
with open('result_f_rs.pkl','rb') as f:
    data =pickle.load(f)


traj = data.all_detect_to_traj()
kal =[]

for i in range(len(traj[0])):
    kal.append([traj[0][i],traj[1][i],traj[2][i]])

traj2 = data.traj
google_earth = []
kml_trajectory= simplekml.Kml()

min = traj2[3].min()
for lat,lon,height in zip(traj2[1],traj2[2],traj2[3]):
    google_earth.append((60+(lat/700),(60+lon/700),(height-min)*15))

ls = kml_trajectory.newlinestring(name = "")
ls.coords = google_earth
ls.extrude = 1
ls.altitudemode = simplekml.AltitudeMode.relativetoground
ls.style.linestyle.color = simplekml.Color.gold

kml_trajectory.save("drone_trajectory_3d.kml")

kal = iterate(kal,5)
kal2=[[] for i in range(3)]
for aa in kal:
    #if aa[1] >=5:
    kal2[0].append(aa[0])
    kal2[1].append(aa[1])
    kal2[2].append(aa[2])
kal2 = np.array(kal2)

vis.show_trajectory_3D(kal2)

kml_tra2= simplekml.Kml()
kamlan_traj = []
for lat,lon,height in zip(kal2[0],kal2[1],kal2[2]):
     kamlan_traj.append((60+(lat/700),(60+lon/700),(height-min)*15))

ls = kml_tra2.newlinestring(name = "")
ls.coords = google_earth
ls.extrude = 1
ls.altitudemode = simplekml.AltitudeMode.relativetoground
ls.style.linestyle.color = simplekml.Color.greenyellow


kml_tra2.save("test2.kml")
