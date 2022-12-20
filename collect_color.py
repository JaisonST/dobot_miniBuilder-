import pygame 
import pygame.camera 

def get_color():
	pygame.init()
	pygame.camera.init()
	
	cam = pygame.camera.Camera('/dev/video0', (640, 480))
	cam.start()
	img = cam.get_image()
	
	[r, g, b, a] = img.get_at((320, 240))
	vals = [r,g,b]
	index = vals.index(max(vals))
	
	return index

print(get_color())


