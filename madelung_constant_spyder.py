# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 08:53:09 2021

@author: NEELKANTH RAWAT
"""
#this program is to evaluate the madelung constant
import numpy as np

#following function takes shape of the 3-d matrix as an argument and returns a 3-d matrix whose elements are values inside the square_root
def dist_block_matrix(shape_tuple):
    sheet_matrix=np.zeros(shape_tuple,dtype=np.float)
    lowest_sheet_shape=np.shape(sheet_matrix[0,:,:])#(no_of_rows,no_of_cols)
    #evaluting sheet_matrix[0,:,0]. rest of the elements can be easily evaluated from it
    for j in range(1,lowest_sheet_shape[0],1):
        sheet_matrix[0,j,0]=sheet_matrix[0,j-1,0]+((2*(j))-1)
    
    #evaluating all the elements of the lowest sheet
    for j in range(1,lowest_sheet_shape[1],1):
        sheet_matrix[0,:,j]=sheet_matrix[0,:,j-1]+( (2*j)-1 )
        
    #now filling values in rest of the sheets
    shape_of_block=np.shape(sheet_matrix)
    for sheet_no in range(1,shape_of_block[0],1):#np.shape(sheet_matrix)=(no. of stacks, no. of rows in each stack, no. of cols in each stack)
        sheet_matrix[sheet_no,:,:]=sheet_matrix[sheet_no-1,:,:]+ np.ones( (shape_of_block[1],shape_of_block[2] ) ,dtype=np.float)*( (2*sheet_no) -1 )
    #print("final sheet_matrix is");print(sheet_matrix)
    return sheet_matrix

#extracting elements lying in the y-z plane(excluding the z axis) #their multiplicity is 8
def yz_plane_excluding_z_axis(amat): 
    shape_of_amat=np.shape(amat)
    #print("elements lying in the y-z plane(excluding the z axis)")
    yz_plane_exclud_z=amat[ 0:shape_of_amat[0],0,1:shape_of_amat[2] ]
    #print(yz_plane_exclud_z)
    return yz_plane_exclud_z

#extracting elements lying in the diagonal plane (excluding elements lying in the z axis) #their multiplicity is 8
def diag_plane_excluding_z_axis(bmat):
    shape_of_bmat=np.shape(bmat)
    #print("elements lying in the diagonal sheet excluding the z axis.")
    diag_plane_exclud_z=np.zeros((shape_of_bmat[1]-1,shape_of_bmat[0]))#initialising the matrix
    for rows in range(0,np.shape(diag_plane_exclud_z)[0],1):#no. of rows for diag_sheet_without_z_axis would be = no. of stacks
        diag_plane_exclud_z[rows,:]=bmat[:,rows+1,rows+1]
    #print(diag_plane_exclud_z)
    return diag_plane_exclud_z

#extracting elements lying in the z axis #their multiplicity is 2
def z_axis_elements(cmat):   
    z_axis=cmat[:,0,0]
    #print("elements lying in the z axis")
    #print(z_axis)
    return z_axis

#creating list of elements which have multiplicity of 16 
# the method used here is very un-pythonic, not-so-numpy like. Will improve it later
def elements_with_multiplicity_16(dmat):
    shape_of_dmat=np.shape(dmat)
    a=[]
    for k in range(0,shape_of_dmat[0],1):
        for i in range(2,shape_of_dmat[1],1):
            for j in range(1,i,1):
                a.append(dmat[k,i,j])
    #print("elements whose multiplicity is 16")
    #print(a) 
    #print("total number of elements whose multiplicity is 16 = ",len(a))
    return a

#main program
shape_dist_3d_mat=(4,4,4)#(no. of stacks, no. of rows in each stack, no. of cols in each stack)
dist_3d_mat=dist_block_matrix(shape_dist_3d_mat)
print("dist_3d_matrix_is")
print(dist_3d_mat)

z_axis_elms=z_axis_elements(dist_3d_mat)
print("z axis elements")
print(z_axis_elms)
mult_16=elements_with_multiplicity_16(dist_3d_mat)
print("elements with multiplicity 16")
print(mult_16)
yz_plane_ex_z=yz_plane_excluding_z_axis(dist_3d_mat)
print("elements on yz plane excluding the z axis")
print(yz_plane_ex_z)
diag_without_z_plane=diag_plane_excluding_z_axis(dist_3d_mat)
print("diagonal plane elements (excluding the z axis)")
print(diag_without_z_plane)
#(1) now i need to define some functions to make my code more clean and readable
#(2) all i need now is to count the number of elements of given value and evaluate the series of madelung constant
#np.count_nonzero(m==x)
#listname.count(value)