import gtk 

def FileChooser (path = None, main_window = None):
    """ Function doc """
    filename = None
    chooser = gtk.FileChooserDialog("Open File...",   main_window             ,
                                    gtk.FILE_CHOOSER_ACTION_OPEN              ,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK)     )
    
    filter = gtk.FileFilter()  
    filter.set_name("MOL2 - SYBIL *.mol2")
    #
    filter.add_mime_type("MOL2 - SYBYL *.mol2")
    filter.add_pattern("*.mol2")
    #
    chooser.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name("PDB files  - *.pdb")
    filter.add_pattern("*.pdb")
    #
    chooser.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name("pDynamo pkl files  - *.pkl")
    filter.add_pattern("*.pkl")
    #
    chooser.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name("pDynamo yaml files  - *.yaml")
    filter.add_pattern("*.yaml")
    
    chooser.add_filter(filter)
    filter = gtk.FileFilter()
    filter.set_name("All files")
    filter.add_pattern("*")
    #
    chooser.add_filter(filter)  
    # chooser.set_current_folder(data_path)
    
    if path != None:
        chooser.set_current_folder(path)
    response = chooser.run()
    if response == gtk.RESPONSE_OK:
        filename = chooser.get_filename()
        chooser.destroy()
    else:
        chooser.destroy()
    return filename  
