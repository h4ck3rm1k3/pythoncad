
from Generic.Kernel.pycadkernel import PyCadDbKernel

#from Generic.Kernel.pycadsettings import PyCadSettings
#from Interface.Wx.quadtree import Quadtree


class Document(object):
    """
    The Document is the interface to the cad kernel.
    The spatial index (quad tree's) are in the Document.
    For on screen display see the ViewPort class.
    """
    def __init__(self, parent, viewport):
        # list of display layers
        self._layers_display = {}
        # reference to the cad window
        self._cadwindow = parent
        # cad kernel is created on file open
        self._cadkernel = None
        # viewport reference
        self._viewport = viewport
        # make the document known to the view
        viewport.Document = self
        # register document commands
        self._RegisterCommands()


    def __GetKernel(self):
        return self._cadkernel

    Kernel = property(__GetKernel, None, None, "Gets the kernel")

    
    def _RegisterCommands(self):
        self._cadwindow.RegisterCommand("REBUILD_IX", self.OnRebuildIndex)
        self._cadwindow.RegisterCommand("REGEN", self.OnRegen)
        self._cadwindow.RegisterCommand("UNDO", self.OnUndo)
        self._cadwindow.RegisterCommand("REDO", self.OnRedo)
        
        
#-------------------- Command handlers ----------------------#
        
    def OnRebuildIndex(self):
        """
        Rebuilds the spatial index for all entities in the database
        """
        if self._cadkernel is not None:
            # index object
            index = self._cadkernel.getSpIndex()
            
            if index is not None:
                print "index constructed"
                # get transaction object
                transaction = index.GetTransaction()
                # remove current content
                index.RemoveAll(transaction)
                # get all entities from the database
                entities = self._cadkernel.getEntityFromType('SEGMENT')
                # traverse each layer in the list
                for entity in entities:
                    # add entity to index
                    index.Insert(transaction, entity.getId(), entity.getBBox())
                transaction.Close(True)
    
                print "index rebuild"
            else:
                print "error rebuilding index"
            

    def OnUndo(self):
        """
            perform the undo command
        """
        try:
            if self._cadkernel is not None:            
                print "-->>Perform unDo"
                self._cadkernel.unDo()  
                self.Regen() 
        except UndoDb:
            print "----<<Err>>No more unDo to performe"
            
            
    def OnRedo(self):
        """
            perform the redo command
        """
        try:
            if self._cadkernel is not None:            
                print "-->>Perform Redo"
                self._cadkernel.reDo() 
                self.Regen() 
        except UndoDb:
            print "----<<Err>>No more redo to performe"

        
    def OnRegen(self):
        """
        Rebuild display lists and redraw the viewport
        """
        if self._cadkernel is not None:
            # get all entities from the database
            entities = self._cadkernel.getEntityFromType('SEGMENT')
            # traverse each layer in the list
            for entity in entities:
                # add entity to view port
                self._viewport.AddEntity(entity)
        

        
#-------------------- Command handlers ----------------------#

    
    def Open(self, filename):
        # todo: check filename

        # open a new kernel
        print "before open"
        self._cadkernel = PyCadDbKernel(filename)
        print "after open"
        #if self._cadkernel.getEntityFromType('SEGMENT'):
        if self._cadkernel.haveDrawingEntitys():
            # create a spatial index
            #self._cadwindow.SendExpression("REBUILD_IX")
            # build display list
            self._cadwindow.SendExpression("REGEN")
            # draw all items
            self._cadwindow.SendExpression("ZOOMA")
        

    def Import(self, fileName):
        """
            import a specifie file
        """
        if not self._cadkernel:
            raise TypeError, "open a file before import a file"
        self._cadkernel.importExternalFormat(fileName)
        # create a spatial index
        self._cadwindow.SendExpression("REBUILD_IX")
        # build display list
        self._cadwindow.SendExpression("REGEN")
        # draw all items
        self._cadwindow.SendExpression("ZOOMA")
        
        
    def GetDrawingExtents(self):
        """
        Gets the min_x, min_y, max_x, max_y for all entities
        """
        if self._cadkernel is not None:
            # index object
            index = self._cadkernel.getSpIndex()
            
            if index is not None:
                # get transaction object
                transaction = index.GetTransaction()
                # get the extents from the index
                return index.GetExtents(transaction)
        # default        
        return (0,0,1,1)


