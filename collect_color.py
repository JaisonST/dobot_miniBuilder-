import pygame 
import pygame.camera 

def get_color():
	pygame.init()
	pygame.camera.init()
	
	cam = pygame.camera.Camera('/dev/video0', (640, 480))
	cam.start()
	img = cam.get_image()

	scrn = pygame.display.set_mode((640, 480))
	pygame.display.set_caption('image')
	scrn.blit(img, (0,0))
	pygame.display.flip()
	
	[r, g, b, a] = img.get_at((320, 240))
	vals = [r,g,b]
	index = vals.index(max(vals))
	
	return index

print(get_color())


