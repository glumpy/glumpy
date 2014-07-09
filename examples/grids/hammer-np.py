import math
import numpy as np
import matplotlib.pyplot as plt



class Hammer(object):

    def forward(self, P):
        longitude = P[:,0]
        latitude = P[:,1]
        cos_lat = np.cos(latitude)
        sin_lat = np.sin(latitude)
        cos_lon = np.cos(longitude/2)
        sin_lon = np.sin(longitude/2)
        D = np.sqrt(1 + cos_lat * cos_lon)
        P_ = np.empty_like(P)
        P_[:,0] = (2 * math.sqrt(2) * cos_lat * sin_lon) / D
        P_[:,1] =     (math.sqrt(2) * sin_lat) / D
        return P_

    def inverse(self,P):
        X = P[:,0]
        Y = P[:,1]
        Z = 1 - (X/4)**2 - (Y/2)**2
        Z = np.where(Z > 0.0, np.sqrt(Z), np.nan)
        P_ = np.empty_like(P)
        P_[:,0] = 2*np.arctan( (Z*X)/(2*(2*Z*Z - 1)) )
        P_[:,1] = np.arcsin(Z*Y)
        return P_


H = Hammer()

n = 512

P = np.zeros((n,n,4))
X_ = np.linspace(-np.pi,   +np.pi ,  n, endpoint=True)
Y_ = np.linspace(-np.pi/2, +np.pi/2, n)
P[...,0], P[...,1] = np.meshgrid(X_,Y_)
P[...,:2] = H.forward(P[...,:2].reshape(n*n,2)).reshape(n,n,2)

X_ = np.linspace(-3.0, +3.0, n)
Y_ = np.linspace(-1.5, +1.5, n)
P[...,2], P[...,3] = np.meshgrid(X_,Y_)
P[...,2:] = H.inverse(P[...,2:].reshape(n*n,2)).reshape(n,n,2)


plt.imshow(P)
plt.show()


"""
for i in np.linspace(1,n,20)-1:
    X,Y = P[i,:,0],P[i,:,1]
    plt.plot(X,Y,c='k',lw=.5)
    X,Y = P[:,i,0],P[:,i,1]
    plt.plot(X,Y,c='k',lw=.5)

plt.show()
"""



# for lat in np.linspace(-np.pi/2,np.pi/2,n,endpoint=True):
#     X = []
#     Y = []
#     for lon in np.linspace(-np.pi,np.pi,n*10,endpoint=True):
#         # print lat, lon
#         x,y = hammer_forward( (lon,lat) )
#         xmin = min(x,xmin)
#         xmax = max(x,xmax)
#         ymin = min(y,ymin)
#         ymax = max(y,ymax)
#         X.append(x)
#         Y.append(y)
#     plt.plot(X,Y)

# for lon in np.linspace(-np.pi,np.pi,n,endpoint=True):
#     X = []
#     Y = []
#     for lat in np.linspace(-np.pi/2,np.pi/2,n*10,endpoint=True):
#         # print lat, lon
#         x,y = hammer_forward( (lon,lat) )
#         xmin = min(x,xmin)
#         xmax = max(x,xmax)
#         ymin = min(y,ymin)
#         ymax = max(y,ymax)
#         X.append(x)
#         Y.append(y)
#     plt.plot(X,Y)
# plt.show()


# print xmin, xmax
# print ymin, ymax
# print

# lonmin,lonmax = 0,0
# latmin,latmax = 0,0

# for x in np.linspace(-4,4,n):
#     for y in np.linspace(-1.5,1.5,n):
#         lon, lat = hammer_inverse( (x,y) )

#         if lon is not np.inf:
#             lonmin = min(lon,lonmin)
#             lonmax = max(lon,lonmax)
#         if lat is not np.inf:
#             latmin = min(lat,latmin)
#             latmax = max(lat,latmax)
#         #print lon, lat
#         #print lon, lat
#         #print hammer_inverse(x,y)
#         # print
# print lonmin, lonmax
# print latmin, latmax
