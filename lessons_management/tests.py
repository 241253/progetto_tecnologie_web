from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from lessons_management.models import Lesson, Packet
from lessons_management.validators import validate_file_extension

# controllo che la funzione validate_file_extention ritorni
# i valori aspettati a fronte di diversi tipi di input
# (corretti oppure no)
class ValidateFileExtentionTest(TestCase):

    def test_bad_file_extension(self):
        '''
             se il file inserito non è un video oppure è un video non in formato mp4
             controlllo che la funzione sollevi l'eccezione corrispondente (ValidationError)
        '''
        video = open('./static/img/logo.png', "r")
        with self.assertRaises(ValidationError):
            validate_file_extension(video)

    def test_right_file_extension(self):
        '''
             se il file inserito è un video in formato.mp4
             controllo che la funzione ritorni il valore True
        '''
        video = open('./uploaded_files/video_lessons/indovina.mp4', "w")
        self.assertTrue(validate_file_extension(video))

# controllo che la funzione set_normalized_difficulty imposti
# correttamente il valore della difficoltà del pacchetto in base
# al valore della difficoltà media calcolata sulla base delle
# lezioni che gli viene passata come parametro
class NormalizedDifficultyRangeTest(TestCase):

    def setUp(self):
        '''
            istanzio il formatore proprietario dei pacchetti e delle lezioni che creo nel corso dei test
        '''
        self.formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password')

    def test_difficulty_facile_base(self):
        '''
            creo un pacchetto la cui difficoltà media (dovuta alle videolezioni inserite)
            è minore di 1.5 e mi aspetto che la set_normalized_difficulty imposti ad 1.0 la difficoltà
        '''
        #creo 5 lezioni con relativa difficoltà
        lessons_list = list()
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 1', description='descrizione lezione 1', difficulty='1.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 2', description='descrizione lezione 2', difficulty='2.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 3', description='descrizione lezione 3', difficulty='2.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 4', description='descrizione lezione 4', difficulty='1.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 5', description='descrizione lezione 5', difficulty='1.0', genre='A', price=20.0))
        #creo il pacchetto contenente le 5 lezioni
        packet = Packet.objects.create(user=self.formatore, title='Titolo pacchetto', description='Descrizione pacchetto')
        packet.lessons.set(lessons_list)
        #chiamo il metodo set_normalize_difficulty per impostare la difficoltà basandosi sulla media delle lezioni inserite
        packet.set_normalize_difficulty()

        #testo che la difficoltà calcolata rientri nel caso 1.0 (Facile Base) visto che la difficolta media (1.4) è minore di 1.5
        self.assertEqual(packet.difficulty, '1.0')

    def test_difficulty_facile_avanzato(self):
        '''
            creo un pacchetto la cui difficoltà media (dovuta alle videolezioni inserite)
            è compresa tra 1.5 (incluso) e 2.5 e mi aspetto che la set_normalized_difficulty
            imposti ad 2.0 la difficoltà
        '''
        #creo 5 lezioni con relativa difficoltà
        lessons_list = list()
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 1', description='descrizione lezione 1', difficulty='1.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 2', description='descrizione lezione 2', difficulty='2.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 3', description='descrizione lezione 3', difficulty='2.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 4', description='descrizione lezione 4', difficulty='2.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 5', description='descrizione lezione 5', difficulty='1.0', genre='A', price=20.0))
        #chiamo il metodo set_normalize_difficulty per impostare la difficoltà basandosi sulla media delle lezioni inserite
        packet = Packet.objects.create(user=self.formatore, title='Titolo pacchetto', description='Descrizione pacchetto')
        packet.lessons.set(lessons_list)
        #chiamo il metodo set_normalize_difficulty passando la difficoltà media delle 5 lezioni
        packet.set_normalize_difficulty()

        #testo che la difficoltà calcolata rientri nel caso 1.0 (Facile Base)
        # visto che la difficolta media (1.6) è compresa tra 1.5 incluso e 2.5
        self.assertEqual(packet.difficulty, '2.0')

    def test_difficulty_medio_base(self):
        '''
            creo un pacchetto la cui difficoltà media (dovuta alle videolezioni inserite)
            è compresa tra 2.5 (incluso) e 3.5 e mi aspetto che la set_normalized_difficulty
            imposti ad 3.0 la difficoltà
        '''
        #creo 5 lezioni con relativa difficoltà
        lessons_list = list()
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 1', description='descrizione lezione 1', difficulty='2.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 2', description='descrizione lezione 2', difficulty='3.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 3', description='descrizione lezione 3', difficulty='3.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 4', description='descrizione lezione 4', difficulty='3.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 5', description='descrizione lezione 5', difficulty='3.0', genre='A', price=20.0))
        #chiamo il metodo set_normalize_difficulty per impostare la difficoltà basandosi sulla media delle lezioni inserite
        packet = Packet.objects.create(user=self.formatore, title='Titolo pacchetto', description='Descrizione pacchetto')
        packet.lessons.set(lessons_list)
        #chiamo il metodo set_normalize_difficulty passando la difficoltà media delle 5 lezioni
        packet.set_normalize_difficulty()

        #testo che la difficoltà calcolata rientri nel caso 1.0 (Facile Base)
        # visto che la difficolta media (2.8) è compresa tra 2.5 incluso e 3.5
        self.assertEqual(packet.difficulty, '3.0')

    def test_difficulty_medio_avanzato(self):
        '''
            creo un pacchetto la cui difficoltà media (dovuta alle videolezioni inserite)
            è compresa tra 3.5 (incluso) e 4.5 e mi aspetto che la set_normalized_difficulty
            imposti ad 3.0 la difficoltà
        '''
        #creo 5 lezioni con relativa difficoltà
        lessons_list = list()
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 1', description='descrizione lezione 1', difficulty='4.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 2', description='descrizione lezione 2', difficulty='4.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 3', description='descrizione lezione 3', difficulty='4.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 4', description='descrizione lezione 4', difficulty='4.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 5', description='descrizione lezione 5', difficulty='2.0', genre='A', price=20.0))
        #chiamo il metodo set_normalize_difficulty per impostare la difficoltà basandosi sulla media delle lezioni inserite
        packet = Packet.objects.create(user=self.formatore, title='Titolo pacchetto', description='Descrizione pacchetto')
        packet.lessons.set(lessons_list)
        #chiamo il metodo set_normalize_difficulty passando la difficoltà media delle 5 lezioni
        packet.set_normalize_difficulty()

        #testo che la difficoltà calcolata rientri nel caso 1.0 (Facile Base)
        # visto che la difficolta media (3.6) è compresa tra 3.5 incluso e 4.5
        self.assertEqual(packet.difficulty, '4.0')

    def test_difficulty_difficile_base(self):
        '''
            creo un pacchetto la cui difficoltà media (dovuta alle videolezioni inserite)
            è compresa tra 4.5 (incluso) e 5.5 e mi aspetto che la set_normalized_difficulty
            imposti ad 5.0 la difficoltà
        '''
        #creo 5 lezioni con relativa difficoltà
        lessons_list = list()
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 1', description='descrizione lezione 1', difficulty='5.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 2', description='descrizione lezione 2', difficulty='5.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 3', description='descrizione lezione 3', difficulty='5.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 4', description='descrizione lezione 4', difficulty='5.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 5', description='descrizione lezione 5', difficulty='4.0', genre='A', price=20.0))
        packet = Packet.objects.create(user=self.formatore, title='Titolo pacchetto', description='Descrizione pacchetto')
        packet.lessons.set(lessons_list)
        #chiamo il metodo set_normalize_difficulty passando la difficoltà media delle 5 lezioni
        packet.set_normalize_difficulty()

        #testo che la difficoltà calcolata rientri nel caso 1.0 (Facile Base)
        # visto che la difficolta media (4.8) è compresa tra 4.5 incluso e 5.5
        self.assertEqual(packet.difficulty, '5.0')

    def test_difficulty_difficile_avanzato(self):
        '''
            creo un pacchetto la cui difficoltà media (dovuta alle videolezioni inserite)
            è maggiore di 5.5 (incluso) e mi aspetto che la set_normalized_difficulty
            imposti ad 6.0 la difficoltà
        '''
        #creo 5 lezioni con relativa difficoltà
        lessons_list = list()
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 1', description='descrizione lezione 1', difficulty='4.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 2', description='descrizione lezione 2', difficulty='6.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 3', description='descrizione lezione 3', difficulty='6.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 4', description='descrizione lezione 4', difficulty='6.0', genre='A', price=20.0))
        lessons_list.append(Lesson.objects.create(user=self.formatore, title='titolo lezione 5', description='descrizione lezione 5', difficulty='6.0', genre='A', price=20.0))
        #chiamo il metodo set_normalize_difficulty per impostare la difficoltà basandosi sulla media delle lezioni inserite
        packet = Packet.objects.create(user=self.formatore, title='Titolo pacchetto', description='Descrizione pacchetto')
        packet.lessons.set(lessons_list)
        #chiamo il metodo set_normalize_difficulty passando la difficoltà media delle 5 lezioni
        packet.set_normalize_difficulty()

        #testo che la difficoltà calcolata rientri nel caso 1.0 (Facile Base)
        # visto che la difficolta media (5.6) è maggiore o uguale a 5.5
        self.assertEqual(packet.difficulty, '6.0')