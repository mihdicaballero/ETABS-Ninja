# -*- coding: utf-8 -*-
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from etabsninja.general_functions import *
from colorama import Fore, Style

def get_story_data(SapModel):
    """
    returns:
    story_data (list). The is a nested list with each element consists of
    [story_nm,story_ele,story_hgt,is_master_story,similar_to,splice_above,
     splice_height]
    """
    #Get the data using API
    story_in=SapModel.Story.GetStories()
    #Separate the data to lists
    nos_stories=story_in[0];
    story_nms=story_in[1];
    story_eles=story_in[2];
    story_hgts=story_in[3];
    is_master_story=story_in[4];
    similar_to_story=story_in[5];
    splice_above=story_in[6];
    splice_height=story_in[7];
    # Create a dictionary to hold the data
    story_data_dict = {
        'Name': story_nms[::-1],
        'Elevation (in)': [round(ele, 3) for ele in story_eles[::-1]],
        'Story height (in)': [round(hgt, 3) for hgt in story_hgts[::-1]],
        'Master Story': is_master_story[::-1],
        'Similar to': similar_to_story[::-1],
        'Splice above': splice_above[::-1],
        'Splice height': splice_height[::-1]
    }
    
    # Create a DataFrame from the dictionary
    story_data = pd.DataFrame(story_data_dict)
    return story_data

def get_all_frames(SapModel):
    """
    Returns:
    frames_data (DataFrame): A DataFrame with data of all frames.
    """
    # Get the frame objects using the API
    frame_objs = SapModel.FrameObj.GetAllFrames()
    
    # Create an empty list to hold frame data
    frames = []
    
    # Populate the frames list with data from frame_objs
    for i in range(frame_objs[0]):
        frameNm = frame_objs[1][i]
        prop = frame_objs[2][i]
        story = frame_objs[3][i]
        pt1 = frame_objs[4][i]
        pt2 = frame_objs[5][i]
        x1 = frame_objs[6][i]
        y1 = frame_objs[7][i]
        z1 = frame_objs[8][i]
        x2 = frame_objs[9][i]
        y2 = frame_objs[10][i]
        z2 = frame_objs[11][i]
        rot = frame_objs[12][i]
        offX1 = frame_objs[13][i]
        offY1 = frame_objs[14][i]
        offZ1 = frame_objs[15][i]
        offX2 = frame_objs[16][i]
        offY2 = frame_objs[17][i]
        offZ2 = frame_objs[18][i]
        cardPt = frame_objs[19][i]
        
        frames.append([
            frameNm, prop, story,
            pt1, pt2,
            x1, y1, z1,
            x2, y2, z2,
            rot,
            offX1, offY1, offZ1,
            offX2, offY2, offZ2,
            cardPt
        ])
    
    # Create a DataFrame from the list
    columns = [
        'Frame Name', 'Property', 'Story',
        'Point 1', 'Point 2',
        'X1', 'Y1', 'Z1',
        'X2', 'Y2', 'Z2',
        'Rotation',
        'Offset X1', 'Offset Y1', 'Offset Z1',
        'Offset X2', 'Offset Y2', 'Offset Z2',
        'Cardinal Point'
    ]
    frames_data = pd.DataFrame(frames, columns=columns)
    
    return frames_data

def get_all_materials(SapModel):
    """
    Gets the materials in the current model. Will return in units mm, N & MPa.
    
    If the property type is either 'Concrete' or 'Steel', the function will
    be expanded so that the strength of materials are included.
    
    Returns
    materials : Type dict
    """
    # Set the Etabs units, all strength of materials will be returned in MPa
    # SapModel.SetPresentUnits(9);
    # switch to k-in units
    kip_in_F = 3
    ret = SapModel.SetPresentUnits(kip_in_F)

    # Etabs material type enumerators
    mat_types={1:'Steel',2:'Concrete',3:'NoDesign',4:'Aluminum',5:'ColdFormed',
               6:'Rebar',7:'Tendon',8:'Masonry'}; 
    mat_name_list=SapModel.PropMaterial.GetNameList();
    materials={};
    for i in range(mat_name_list[0]):
        mat_name=mat_name_list[1][i];
        mat_props=SapModel.PropMaterial.GetMaterial(mat_name);
        mat_type=mat_types[mat_props[0]];
        if(mat_type=='Concrete'):
            mat_conc_prop=SapModel.PropMaterial.GetOConcrete_1(mat_name);
            conc_fc=mat_conc_prop[0];
            materials[mat_name]={'mat_name':mat_name,'mat_type':mat_type,
                                 'fc':conc_fc};
        elif(mat_type=='Steel'):
            mat_steel_prop=SapModel.PropMaterial.GetOSteel_1(mat_name);
            steel_fy=mat_steel_prop[0];
            steel_fu=mat_steel_prop[1];
            materials[mat_name]={'mat_name':mat_name,'mat_type':mat_type,
                                 'fy':steel_fy,'fu':steel_fu};
        else:
            materials[mat_name]={'mat_name':mat_name,'mat_type':mat_type};
    return materials;

def get_all_points(SapModel,inc_restraint=True):
    """
    This will return all the points of the model.
    
    Parameters:
    SapModel : SapModel.Pointer
    inc_restraint : boolean (set True for restraints to be included
                             to points list)
    units : str. Default to 'mm'
    
    Returns:
    points : list (Points in current Etabs model). Elements in the points
    list if inc_restraint==False [pt_nm,x,y,z]. If inc_restraint==True the
    point element = [pt_nm,x,y,z,(FUx,FUy,FUz,FRx,FRy,FRz)]
    """
    [numberPts,ptNames,ptX,ptY,ptZ,ptCsys]=SapModel.PointObj.GetAllPoints();
    #initiate a temporary list to contain the restrained points data
    ptsRestraint=[];
    if(inc_restraint==True):
        for i in range(numberPts):
            ptRestraintSA=SapModel.PointObj.GetRestraint(ptNames[i]);
            ptRestraint=ptRestraintSA[0];
            ptsRestraint.append(ptRestraint);
    #Initiate the points list
    points=[]
    for i in range(numberPts):
        if(inc_restraint==True):
            points.append([ptNames[i],ptX[i],ptY[i],ptZ[i],ptsRestraint[i]]);
        else:
            points.append([ptNames[i],ptX[i],ptY[i],ptZ[i]]);
    # Define column names
    if inc_restraint:
        columns = ['Point Name', 'X', 'Y', 'Z', 'Restraint']
    else:
        columns = ['Point Name', 'X', 'Y', 'Z']
    
    # Create a DataFrame from the list
    points_data = pd.DataFrame(points, columns=columns)
    
    return points_data

def get_StoryDriftsForStories(SapModel, LoadCaseList=["Dead"], predefined_max_drift = 0.0025):
    """
    returns:
    df (DataFrame). A data frame with all the drifts of the stories for a single case. 
    """
    #Get the data using API
    SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(LoadCaseList)
    TableName = "Story Drifts"
    TableFields = SapModel.DatabaseTables.GetAllFieldsInTable(TableName)[2]
    JointDrifts = SapModel.DatabaseTables.GetTableForDisplayArray(TableName, TableFields, "All")[4]
    TableFieldsIncluded = SapModel.DatabaseTables.GetTableForDisplayArray(TableName, TableFields, "All")[2]
    # Determine the number of columns
    NumColumns = len(TableFieldsIncluded)

    # Reshape the JointDrifts list into a 2D array with the appropriate dimensions
    joint_drifts_array = [JointDrifts[i:i+NumColumns] for i in range(0, len(JointDrifts), NumColumns)]

    # Create the DataFrame using the reshaped array and the column names
    df = pd.DataFrame(joint_drifts_array, columns=TableFieldsIncluded)

    # Convert 'Drift' column to float
    df[['Drift']] = df[['Drift']].astype(float)

    # Group the DataFrame by 'Story' and calculate the minimum and maximum values of 'Drift'
    df = df.groupby(['Story','Direction'])[['Drift']].agg(['max'])

    # Flatten the column names by joining them with an underscore
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

    # Reset the index to make 'Story' a regular column
    df.reset_index(inplace=True)

    # Pivot the DataFrame to create separate columns for 'DriftX' and 'DriftY' values
    df = df.pivot(index='Story', columns='Direction', values='Drift_max').reset_index()

    # Rename the columns
    df.columns = ['Story', 'DriftX_max', 'DriftY_max']

    # Sort the DataFrame by 'Story' column in alphabetical order
    df = df.sort_values('Story', ascending=True)

    # Create a scatter plot with lines connecting the points
    plt.plot(df['DriftX_max'], df['Story'], label='DriftX_max')
    plt.plot(df['DriftY_max'], df['Story'], label='DriftY_max')

    # Add labels and title
    plt.xlabel('Drift')
    plt.title('Drift vs. Story')
    # Add a legend
    plt.legend()

    # Get the maximum value of Drifts
    max_drift_x = df['DriftX_max'].max()
    max_drift_y = df['DriftY_max'].max()

    bold_terminal("Story drift for stories check")
    FU("Drift X", max_drift_x, predefined_max_drift)
    FU("Drift Y", max_drift_y, predefined_max_drift)

    return df

def get_StoryDriftsForJoints(SapModel, LoadCaseList=["Dead"], GroupName="All", predefined_max_drift = 0.0025):
    """
    returns:
    df (DataFrame). A data frame with all the drifts of selected column Joints for all the stories. 
    test
    """
    JointsGroupName = GroupName # Put "All" for all nodes of the model
    TableName = "Joint Drifts"
    SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(LoadCaseList)
    TableFields = SapModel.DatabaseTables.GetAllFieldsInTable(TableName)[2]
    JointDrifts = SapModel.DatabaseTables.GetTableForDisplayArray(TableName, TableFields, JointsGroupName)[4]
    TableFieldsIncluded = SapModel.DatabaseTables.GetTableForDisplayArray(TableName, TableFields, "All")[2]

    # Determine the number of columns
    NumColumns = len(TableFieldsIncluded)

    # Reshape the JointDrifts list into a 2D array with the appropriate dimensions
    joint_drifts_array = [JointDrifts[i:i+NumColumns] for i in range(0, len(JointDrifts), NumColumns)]

    # Create the DataFrame using the reshaped array and the column names
    df = pd.DataFrame(joint_drifts_array, columns=TableFieldsIncluded)
    # Convert 'DriftX' and 'DriftY' columns to float
    df[['DriftX', 'DriftY']] = df[['DriftX', 'DriftY']].astype(float)

    # Group the DataFrame by 'Story' and calculate the minimum and maximum values of 'DriftX' and 'DriftY'
    df = df.groupby('Story')[['DriftX', 'DriftY']].agg(['max'])

    # Flatten the column names by joining them with an underscore
    df.columns = ['_'.join(col).strip() for col in df.columns.values]

    # Reset the index to make 'Story' a regular column
    df.reset_index(inplace=True)

    # Sort the DataFrame by 'Story' column in alphabetical order
    df = df.sort_values('Story', ascending=True)

    # Create a scatter plot with lines connecting the points
    plt.figure()
    plt.plot(df['DriftX_max'], df['Story'], label='DriftX_max')
    plt.plot(df['DriftY_max'], df['Story'], label='DriftY_max')

    # Add labels and title
    plt.xlabel('Drift')
    plt.title('Drift vs. Story')
    # Add a legend
    plt.legend()

    # Get the maximum value of Drifts
    max_drift_x = df['DriftX_max'].max()
    max_drift_y = df['DriftY_max'].max()

    bold_terminal("Story drift for selected joints check")
    FU("Drift X", max_drift_x, predefined_max_drift)
    FU("Drift Y", max_drift_y, predefined_max_drift)
    
    return df

def get_DiaphragmCMDisplacements(SapModel, LoadCaseList=["Dead"], building_height = 100,max_BuildingDrift=1/400):
    """
    Parameters:
        SapModel: Active SapModel to get results from.
        LoadCaseList (list): List of load cases to get results from. 
        building_height (int): Total building height, in ft.
        max_BuildingDrift (float): Maximum alllowable building drift.
    returns:
    df (DataFrame). A data frame with all the Center of Mass displacement of the stories for a list of cases. 
    """
    #Get the data using API
    SapModel.DatabaseTables.SetLoadCasesSelectedForDisplay(LoadCaseList)
    TableFields = SapModel.DatabaseTables.GetAllFieldsInTable('Diaphragm Center Of Mass Displacements')[3]
    CMDisplacements = SapModel.DatabaseTables.GetTableForDisplayArray('Diaphragm Center Of Mass Displacements', TableFields, "All")[4]
    TableFieldsIncluded = SapModel.DatabaseTables.GetTableForDisplayArray('Diaphragm Center Of Mass Displacements', TableFields, "All")[2]

    # Determine the number of columns
    NumColumns = len(TableFieldsIncluded)

    # Reshape the JointDrifts list into a 2D array with the appropriate dimensions
    CMDisplacements_array = [CMDisplacements[i:i+NumColumns] for i in range(0, len(CMDisplacements), NumColumns)]
    # Create the DataFrame using the reshaped array and the column names
    df = pd.DataFrame(CMDisplacements_array, columns=TableFieldsIncluded)

    # Convert 'UY' and 'UY column to float
    df[['UX','UY']] = df[['UX','UY']].astype(float)

    # Group the DataFrame by 'Story' and calculate the minimum and maximum values of 'Drift'
    # df = df.groupby(['Story'])[['UX', 'UY']].agg(['max','min'])
    df = df.groupby('Story')[['UX', 'UY']].agg(lambda x: abs(x).max())

    # Reset the index to make 'Story' a regular column
    df.reset_index(inplace=True)

    # Sort the DataFrame by 'Story' column in alphabetical order
    df = df.sort_values('Story', ascending=True)

    # Create a scatter plot with lines connecting the points
    plt.figure()
    plt.plot(df['UX'], df['Story'], label='UX_max')
    # plt.plot(df['UX_min'], df['Story'], label='UX_min')
    plt.plot(df['UY'], df['Story'], label='UY_max')
    # plt.plot(df['UY_min'], df['Story'], label='UY_min')

    # Add labels and title
    plt.xlabel('CM Displacement')
    plt.title('CM Displacement vs. Story')
    # Add a legend
    plt.legend()    

    # Get the maximum value of Drifts
    max_displacement_x = df['UX'].max()
    max_displacement_y = df['UY'].max()

    bold_terminal("Diaphragm Center of Mass total displacement check")
    FU("CM Displacement X", max_displacement_x, building_height*12*max_BuildingDrift)
    FU("CM Displacement Y", max_displacement_y, building_height*12*max_BuildingDrift)

    return df
