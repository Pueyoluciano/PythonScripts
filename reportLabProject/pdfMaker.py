from reportlab.pdfgen import canvas  
from reportlab.lib.units import cm  
import math

class pdfCreator:
    """
        This class uses reportLabs capabilities to generate pdfs.
        
        The document's width is setted in dots, wich are equivalent to a 1/72 of an inch.
        
        some equivalences:
        0.3528 mm(1/72 inches)  ---> 1 dot 
        1 mm ----------------------> 2.83 dot
        57 mm ---------------------> 161.56 dot
        
        [!] This class assumes that the template will have fixed width.
            All the content in the template that exceeds the maximum width 
            (calculated using the units mentoined before), will not be 
            rendered properly.
            This is the expected behaviour of the Reportlab functionality.
            
    """
    def __init__(self, file_name="pdfCreatorOutput.pdf", page_size=(161.56, 1200), bottom_up=0, right_margin=0.15*cm, line_height=0.4*cm, template_file="template.txt"):
        self.canvas = canvas.Canvas(filename=file_name, pagesize=page_size, bottomup=bottom_up)
        self.canvas.setFont("Courier", 8)
        self.right_margin = right_margin
        self.line_height = line_height
        self.lines_count = 0
        self.template_file = template_file
        self.template_string = None
        self.parameter_identifier = "&"
    
    def renderTemplate(self, parameters):
        template_file = open(self.template_file, "r")
        self.template_string = template_file.read()
        template_file.close()
        
        #Replace Parameters tokens with actual values
        self._renderParameters(parameters)
        
        #Write the canvas
        self._writeLines()
        
        #Save PDF file
        self._saveCanvas()
        
    def _renderParameters(self, parameters):
        for parameter in parameters:
            self.template_string = self.template_string.replace(self.parameter_identifier + parameter, parameters[parameter])
    
    def _writeLines(self):
        lines = self.template_string.split("\n")
        
        for line in lines:
            self.lines_count += 1
            line_pos = self.lines_count * self.line_height
            self.canvas.drawString(self.right_margin, line_pos, line)  
        
    def _saveCanvas(self):
        self.canvas.showPage()
        self.canvas.save()
        

creator = pdfCreator(file_name="output.pdf")

parametros = {"id": "15",
 "date": "02/01/2018",
 "address": "Lacasa",
 "time": "12311",
 "plate": "ABC131",
 "brand": "LAMBO",
 "color": "ORO",
 "vehicle_type": "CARRUCHO",
 "ticket_category_code": "asd",
 "ticket_category_desc": "asd2",
 "measure_taken": "Tomo el Palo",
 "inspector_name": "Jorge Nestor",
 "inspector_dni": "33111222",
 "notification_type": "Alto Gato"}
 
creator.renderTemplate(parametros)
