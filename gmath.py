import math
from display import *

AMBIENT = 0
DIFFUSE = 1
SPECULAR = 2
LOCATION = 0
COLOR = 1
SPECULAR_EXP = 4

#lighting functions
def get_lighting(normal, view, ambient, light, areflect, dreflect, sreflect ):
    amb = calculate_ambient(ambient, areflect)
    diff = calculate_diffuse(light, dreflect, normal)
    spec = calculate_specular(light, sreflect, view, normal)
    return limit_color([x+y+z for x,y,z in zip(amb,diff,spec)])

def calculate_ambient(alight, areflect):
    return limit_color([x*y for x,y in zip(alight,areflect)])

def calculate_diffuse(light, dreflect, normal):
    lightvec = normalize(light[LOCATION])
    lightcolor = light[COLOR]
    dot = dot_product(lightvec,normalize(normal))
    return limit_color([x*y*dot for x,y in zip(lightcolor,dreflect)])

def calculate_specular(light, sreflect, view, normal):
    lightvec = light[LOCATION]
    lightcolor = light[COLOR]
    constant = 2 * dot_product(lightvec, normal)
    temp = [constant*x-y for x,y in zip(normal, lightvec)]
    constant = dot_product(temp, view) ** 16
    return limit_color([x*y*constant for x,y in zip(lightcolor, sreflect)])

def limit_color(color):
    for i in range(len(color)):
        if color[i] > 255:
            color[i] = 255
        if color[i] < 0:
            color[i] = 0
    return color

#vector functions
def normalize(vector):
    mag = (vector[0]**2 + vector[1]**2 + vector[2]**2) ** 0.5
    return [each/mag for each in vector]

def dot_product(a, b):
    return (a[0]*b[0]) + (a[1]*b[1]) + (a[2]*b[2])

def calculate_normal(polygons, i):

    A = [0, 0, 0]
    B = [0, 0, 0]
    N = [0, 0, 0]

    A[0] = polygons[i+1][0] - polygons[i][0]
    A[1] = polygons[i+1][1] - polygons[i][1]
    A[2] = polygons[i+1][2] - polygons[i][2]

    B[0] = polygons[i+2][0] - polygons[i][0]
    B[1] = polygons[i+2][1] - polygons[i][1]
    B[2] = polygons[i+2][2] - polygons[i][2]

    N[0] = A[1] * B[2] - A[2] * B[1]
    N[1] = A[2] * B[0] - A[0] * B[2]
    N[2] = A[0] * B[1] - A[1] * B[0]

    return N
