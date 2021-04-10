# -*- coding: utf-8 -*-
"""
Created on Sat Mar 20 08:53:09 2021

@author: NEELKANTH RAWAT
"""
#this program is to evaluate the madelung constant (ionic crystals' case)
#not complete et. need to just incorpirate the summation series.
import numpy as np

#following function takes shape of the 3-d matrix as an argument and returns a 3-d matrix whose elements are "square_of(distance from the origin)/((#nearest_nbr_dist=a)**2)
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
def xz_plane_excluding_z_axis(amat): 
    shape_of_amat=np.shape(amat)
    #print("elements lying in the y-z plane(excluding the z axis)")
    # code commented on the next line is old and wrong. i need to avoid elements lying on x-y plane
    #xz_plane_exclud_z=amat[ 0:shape_of_amat[0],0,1:shape_of_amat[2] ]
    xz_plane_exclud_z=amat[ 1:shape_of_amat[0],0,1:shape_of_amat[2] ]#this is correct
    #print(xz_plane_exclud_z)
    return xz_plane_exclud_z

#extracting elements lying in the diagonal plane (excluding elements lying in the z axis) #their multiplicity is 8
def diag_plane_excluding_z_axis(bmat):
    shape_of_bmat=np.shape(bmat)#(no. of stacks, no. of rows, no. of cols)
    '''
    #print("elements lying in the diagonal sheet excluding the z axis.")
    # code commented on the next line is old and wrong. i need to avoid elements lying on x-y plane
    # diag_plane_exclud_z=np.zeros((shape_of_bmat[1]-1,shape_of_bmat[0]))#initialising the matrix
    for rows in range(0,np.shape(diag_plane_exclud_z)[0],1):#no. of rows for diag_sheet_without_z_axis would be = no. of stacks-1
        diag_plane_exclud_z[rows,:]=bmat[:,rows+1,rows+1]
    #print(diag_plane_exclud_z)
    '''
    #initialising the shape of matrix we want to return
    diag_plane_exclud_z=np.zeros((shape_of_bmat[1]-1,shape_of_bmat[0]-1))
    for rows in range(0,np.shape(diag_plane_exclud_z)[0],1):
        diag_plane_exclud_z[rows,:]=bmat[1:shape_of_bmat[0],rows+1,rows+1]
    #done
    return diag_plane_exclud_z

#extracting elements lying in the z axis #their multiplicity is 2
def z_axis_elements(cmat):   
    shape_of_cmat=np.shape(cmat)
    # old value: z_axis=cmat[:,0,0]# this is wrong. i need to ignore elements present on x-y plane(in this case at the origin)
    z_axis=cmat[1:shape_of_cmat[0],0,0]# this is correct.
    #print("elements lying in the z axis")
    #print(z_axis)
    return z_axis

#creating list of elements which have multiplicity of 16 
# the method used here is very un-pythonic, not-so-numpy like. Will improve it later
def elements_with_multiplicity_16(dmat):
    shape_of_dmat=np.shape(dmat)
    a=[]
    for k in range(1,shape_of_dmat[0],1):#i made a change here . k will start from 1 and not 0 (as was mentioned earlier)
        for i in range(2,shape_of_dmat[1],1):
            for j in range(1,i,1):
                a.append(dmat[k,i,j])
    #print("elements whose multiplicity is 16")
    #print(a) 
    #print("total number of elements whose multiplicity is 16 = ",len(a))
    return a

#function to extract the elements present between x axis and diagonal of the lowest sheet matrix as they have multiplicity of 8 and not 16
def xy_plane_els(emat):#these elements have multiplicity of 4
    shape_of_emat=np.shape(emat)
    b=[]
    #method is very unpythonic, very not-so-numpy like. will loof for the better one later
    for i in range(1,shape_of_emat[1],1):
        for j in range(1, i,1):#stop is i because we are not including diagonal elements
            b.append(emat[0,i,j])
    return b

#function to extract elements of x axis and diagonal of the lowest sheet matrix(they have multiplicity of 4)
def mult_4_x_and_diag_els(fmat):
    diag=np.diag(fmat[0,:,:])
    x_axis=fmat[0,:,0]
    ans_return=np.concatenate((diag,x_axis))
    return ans_return


#this function takes "square of (radial distance from the origin)/((#nearest_nbr_dist=a)**2)" and three group of elements of different multiplicity as an input and return number of such points in space consistent with our 3d- mesh(otherwise it woul dhave been infinitiy 'cause)
def how_many_such_pts(dist_val,z_ax_els,xz_plane_els_without_z,diag_plane_without_z,mult_16_els_list,mult_8_xy_list,mult_4_xy_arr):
    num_of_such_points=0;#initialising
    in_z_ax=np.count_nonzero(z_ax_els == dist_val)
    in_xz_plane=np.count_nonzero(xz_plane_els_without_z == dist_val)
    in_diag_plane=np.count_nonzero(diag_plane_without_z== dist_val)
    in_mult_16=mult_16_els_list.count(dist_val)
    in_mult_8_xy_list=mult_8_xy_list.count(dist_val)
    in_mult_4_xy_arr=np.count_nonzero(mult_4_xy_arr==dist_val)
    num_of_such_points=(2*in_z_ax)+(8*in_xz_plane)+(8*in_diag_plane)+(16*in_mult_16)+(8*in_mult_8_xy_list)+(4*in_mult_4_xy_arr)
    return num_of_such_points

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
xz_plane_ex_z=xz_plane_excluding_z_axis(dist_3d_mat)
print("elements on xz plane excluding the z axis")
print(xz_plane_ex_z)
diag_without_z_plane=diag_plane_excluding_z_axis(dist_3d_mat)
print("diagonal plane elements (excluding the z axis)")
print(diag_without_z_plane)
els_xy_plane=xy_plane_els(dist_3d_mat)
print("x-y plane elements")
print(els_xy_plane)
mult_4_elms=mult_4_x_and_diag_els(dist_3d_mat)
print("elements with multiplicity of 4")
print(mult_4_elms)

#testing how many function
print("no. of points at a distance of sqrt(2)*a from the ion at the origin: ",how_many_such_pts(1,z_axis_elms,xz_plane_ex_z,diag_without_z_plane,mult_16,els_xy_plane,mult_4_elms))

#(1) done: now i need to define some functions to make my code more clean and readable. 
#(2) done: all i need now is to count the number of elements of given value and evaluate the series of madelung constant
#np.count_nonzero(m==x)
#listname.count(value)
