from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from sqlalchemy.orm import sessionmaker


class GameAddition(Screen):

    def save_data(self):
        generation = self.generation.text
        game_name = self.game_name.text
        region = self.region.text
        error = self.check_data(generation, game_name, region)
        if error:
            popup = Popup(title="Ошибка заполнения формы",
                          content=Label(text=error),
                          size_hint=(None, None), size=(400, 400)
                          )
            popup.open()
        else:
            dlc = self.dlc.text
            from databases import Game, create_engine
            engine = create_engine()
            local_session = sessionmaker(autoflush=False, autocommit=False, bind=engine)
            session = local_session()
            if self.check_game_name(Game, session, game_name, dlc):
                new_game = Game(
                    generation=int(generation),
                    name=game_name,
                    region=region,
                    dlc=dlc
                )
                session.add(new_game)
                session.commit()
            else:
                popup = Popup(title="Повторная игра!",
                              content=Label(text="Такая игра уже есть в списке!"),
                              size_hint=(None, None), size=(400, 400)
                              )
                popup.open()

    def check_data(self, generation: str, game_name: str, region: str):
        error_message = ''
        if 0 == len(generation):
            error_message += "Не заполнено поле \'Поколение\'!\n"
        elif not generation.isdigit():
            error_message += "В поле \'Поколение\' введено не число!\n"
        if 0 == len(game_name):
            error_message += "Не заполнено поле \'Название игры\'!\n"
        if 0 == len(region):
            error_message += "Не заполнено поле \'Регион\'!\n"
        return error_message

    @staticmethod
    def check_game_name(game, session, game_name: str, dlc):
        if dlc:
            result = session.query(game).where(game.name == game_name, game.dlc == dlc).first()
        else:
            result = session.query(game).where(game.name == game_name).first()
        if result:
            return False
        else:
            return True
