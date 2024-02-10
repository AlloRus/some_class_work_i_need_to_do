import requests, pygame, os, sys


def load_map(lon, lat, delta, api):
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    response = requests.get(api, params=params)
    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return "map.png"


if __name__ == '__main__':

    pygame.init()
    size = w, h = 600, 450
    screen = pygame.display.set_mode(size)
    fps = 60
    running = 1
    clock = pygame.time.Clock()
    lon = 37.588392
    lat = 55.734036
    delta = 0.005
    map_file = ""


    def update_map():
        global map_file, lon
        if lon < -180:
            lon += 360
        elif lon > 180:
            lon -= 360
        map_file = load_map(str(lon), str(lat), str(delta), "http://static-maps.yandex.ru/1.x/")


    update_map()
    while running:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                i = pygame.key.get_pressed()

                if i[pygame.K_PAGEDOWN]:
                    if delta >= 0.00025:
                        delta /= 2
                    update_map()
                if i[pygame.K_PAGEUP]:
                    if delta < 22.5:
                        delta *= 2
                    update_map()

                if i[pygame.K_UP]:
                    if -85 < lat + delta < 85:
                        lat += delta
                    update_map()
                if i[pygame.K_DOWN]:
                    if -85 < lat - delta < 85:
                        lat -= delta
                    update_map()

                if i[pygame.K_LEFT]:
                    lon -= delta * 2.5
                    update_map()
                if i[pygame.K_RIGHT]:
                    lon += delta * 2.5
                    update_map()

        screen.blit(pygame.image.load(map_file), (0, 0))
        clock.tick(fps)
        pygame.display.flip()
    pygame.quit()
os.remove(map_file)
