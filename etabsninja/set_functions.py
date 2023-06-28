
# -*- coding: utf-8 -*-
def create_circular_section(sapmodel, concrete_material, longitudinal_material, tie_material, section_diameter, clear_cover, num_longitudinal_bars, longitudinal_bar_diameter, tie_bar_diameter, tie_spacing):
    # Set section properties
    section_name = f"Circular-Ø{section_diameter}-{concrete_material}-{longitudinal_material}-{num_longitudinal_bars}-{longitudinal_bar_diameter}"
    # Create circular section
    sapmodel.PropFrame.SetCircle(section_name, concrete_material, section_diameter) 
    # Set reinforcement
    ret = sapmodel.FrameObj.SetRebarColumn(section_name, longitudinal_material, tie_material, 2, 1, clear_cover, num_longitudinal_bars, 0,0, longitudinal_bar_diameter, tie_bar_diameter, tie_spacing, 0, 0, False)
    
    if ret == 0:
        print(f"Function 'create_circular_section' was successful")
    else:
        print(f"Error running function 'create_circular_section'")

def create_rectangular_section(sapmodel, concrete_material, steel_material, clear_cover, width, depth):
    # Set section properties
    section_name = f"Rectangular_{concrete_material}_{steel_material}_{clear_cover}_{width}x{depth}"
    sapmodel.PropFrame.SetRectangle(section_name, concrete_material, width, depth)
    
    # Create rectangular section
    sapmodel.FrameObj.AddByCoordinate(0, 0, 0, width, 0, depth, section_name, "", "")
    
    # Set reinforcement
    ret = sapmodel.FrameObj.SetRebarLayout(section_name, "None", "None", 0, "Column", clear_cover, 0, "None", "None", 0, 0, 0)
    
    if ret == 0:
        print(f"Function 'create_rectangular_section' was successful")
    else:
        print(f"Error running function 'create_rectangular_section'")


""" #define material property
MATERIAL_CONCRETE = 2
ret = SapModel.PropMaterial.SetMaterial('CONC', MATERIAL_CONCRETE)

#assign isotropic mechanical properties to material
ret = SapModel.PropMaterial.SetMPIsotropic('CONC', 6000, 0.2, 0.0000055)

 """





