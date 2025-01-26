import arcade


SCREEN_TITLE = "Platformer"

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650


CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING


PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


class MyGame(arcade.Window):


    def __init__(self):


        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,
                         SCREEN_TITLE, resizable=True)

        self.tile_map = None

        self.scene = None

        self.player_sprite = None

        self.physics_engine = None

        self.camera_sprites = None

        self.camera_gui = None

        self.score = 0

        self.left_key_down = False
        self.right_key_down = False
        self.enemy = None
        self.enemy1 = None
        self.exit_player = None
        self.sound = None
        self.music = None
        self.sound_lose = None
        self.sound_win = None
        self.coin_sound = None


    def setup(self):
        self.camera_sprites = arcade.Camera(self.width, self.height)
        self.camera_gui = arcade.Camera(self.width, self.height)
        map_name = ":resources:tiled_maps/map.json"
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)


        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        self.score = 0

        src = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(src, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)


        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"]
        )

        #
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        exit_sprite = ":resources:images/tiles/signExit.png"
        self.exit_player = arcade.Sprite(exit_sprite, CHARACTER_SCALING)
        self.exit_player.center_x = 3000
        self.exit_player.center_y = 128
        self.scene.add_sprite("Exit", self.exit_player)

        enemy_sprite = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.enemy = arcade.Sprite(enemy_sprite, CHARACTER_SCALING)
        self.enemy.center_x = 400
        self.enemy.center_y = 128
        self.scene.add_sprite("Enemy", self.enemy)

        enemy1_sprite = ":resources:images/animated_characters/zombie/zombie_idle.png"
        self.enemy1 = arcade.Sprite(enemy1_sprite, CHARACTER_SCALING)
        self.enemy1.center_x = 1900
        self.enemy1.center_y = 128
        self.scene.add_sprite("Enemy1", self.enemy1)



        self.sound = arcade.load_sound(":resources:music/1918.mp3")
        self.music = arcade.play_sound(self.sound,
                                       volume=0.1,
                                       looping=True)
        self.sound_lose = arcade.load_sound("lose.wav")
        self.sound_win = arcade.load_sound("win.mp3")
        self.coin_sound = arcade.load_sound("coin-sound.mp3")



    def on_draw(self):


        self.clear()

        self.camera_sprites.use()

        self.scene.draw()

        self.camera_gui.use()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text,
                         start_x=10,
                         start_y=10,
                         color=arcade.csscolor.WHITE,
                         font_size=18)

    def update_player_speed(self):

        self.player_sprite.change_x = 0

        if self.left_key_down and not self.right_key_down:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif self.right_key_down and not self.left_key_down:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED

        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = True
            self.update_player_speed()

        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = True
            self.update_player_speed()

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.A:
            self.left_key_down = False
            self.update_player_speed()
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_key_down = False
            self.update_player_speed()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera_sprites.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (self.camera_sprites.viewport_height / 2)
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0

        player_centered = screen_center_x, screen_center_y
        self.camera_sprites.move_to(player_centered)

    def on_update(self, delta_time):

        self.physics_engine.update()

        coin_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Coins"]
        )

        for coin in coin_hit_list:
            arcade.play_sound(self.coin_sound)
            coin.remove_from_sprite_lists()

            self.score += 1




        self.center_camera_to_player()


        if arcade.check_for_collision(self.player_sprite, self.enemy):
            arcade.play_sound(self.sound_lose)
            arcade.pause(1)
            self.player_sprite.kill()
            arcade.close_window()
            print("Вы проиграли")

        if arcade.check_for_collision(self.player_sprite, self.enemy1):
            arcade.play_sound(self.sound_lose)
            arcade.pause(1)
            self.player_sprite.kill()
            arcade.close_window()
            print("Вы проиграли")

        if arcade.check_for_collision(self.player_sprite, self.exit_player):
            arcade.play_sound(self.sound_win)
            arcade.pause(3.1)
            self.player_sprite.kill()
            arcade.close_window()
            print("Вы выйграли!")





    def on_resize(self, width, height):

        self.camera_sprites.resize(int(width), int(height))
        self.camera_gui.resize(int(width), int(height))


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()