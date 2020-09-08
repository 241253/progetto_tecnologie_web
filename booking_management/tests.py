import datetime as dt
from django.contrib.auth.models import User
from django.test import TestCase, Client
from django.urls import reverse
from booking_management.models import Booking, BookingStatus

#test effettuati senza utente loggato
class UserBookingView_NoUserLogin_Test(TestCase):

    def setUp(self):
        '''
            istanzio un client
        '''
        self.client = Client()

    def test_template(self):
        '''
            verifico che il template aperto non sia quello della view
            ma quello che visualizza l'errore di mancato login
            dopo essere stato redirezionato alla pagina giusta
        '''
        response = self.client.get(reverse('user_booking'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateNotUsed(response, 'user_management/user/user_booking.html')
        self.assertTemplateUsed(response, 'registration/login.html')

#test effettuati con utente registrato e già loggato (no staff o superuser)
class UserBookingView_UserLogin_Test(TestCase):

    def setUp(self):
        '''
            istanzio un client,
            creo un utente nel database
            ed effettuo il login con questo utente appena creato
        '''
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
        self.client.login(username='john', password='johnpassword')

    def test_template(self):
        '''
            verifico che il template aperto sia quello corretto
        '''
        response = self.client.get(reverse('user_booking'))
        self.assertTemplateUsed(response, 'user_management/user/user_booking.html')

    def test_no_booking_no_bookingStatus_no_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - non ci siano prenotazioni in attesa di conferma/annullamento
                - non ci siano prenotazioni già confermate/annullate per il futuro
                - non ci siano prenotazioni già confermate/annullate per il passato
            (cioè l'utente ancora non ha mai fatto una prenotazione neanche una volta)
        '''

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertNotContains(response, "Prenotazioni in attesa di conferma")
        #controllo su prenotazioni future già confermate/annullate
        self.assertNotContains(response, "Videolezioni live prenotate")
        self.assertContains(response, "Nessuna videolezione")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertNotContains(response, "Prenotazioni passate")

        #controllo sulle liste del context
        self.assertQuerysetEqual(response.context['booking'], [])
        self.assertQuerysetEqual(response.context['booking_status'], [])
        self.assertQuerysetEqual(response.context['booking_past'], [])

    def test_yes_booking_no_bookingStatus_no_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - ci siano prenotazioni in attesa di conferma/annullamento
                - non ci siano prenotazioni già confermate/annullate per il futuro
                - non ci siano prenotazioni già confermate/annullate per il passato
            (cioè le uniche prenotazioni fatte dall'utente non sono ancora state confermate)
        '''
        #popolazione db per effettuare il test
        booking = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=7)), ora=dt.time(hour=8))

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertNotContains(response, "Videolezioni live prenotate")
        self.assertContains(response, 'Nessuna videolezione')
        #controllo su prenotazioni passate già confermate/annullate
        self.assertNotContains(response, "Prenotazioni passate")

        #controllo sulle liste del context
        booking_list = ['<Booking: ' + booking.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking'], booking_list)
        self.assertQuerysetEqual(response.context['booking_status'], [])
        self.assertQuerysetEqual(response.context['booking_past'], [])

    def test_no_booking_yes_bookingStatus_no_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - non ci siano prenotazioni in attesa di conferma/annullamento
                - ci siano prenotazioni già confermate/annullate per il futuro
                - non ci siano prenotazioni già confermate/annullate per il passato
            (cioè le uniche prenotazioni fatte dall'utente sono state confermate/annullate
            e hanno una data futura rispetto ad oggi)
        '''
        #popolazione db per effettuare il test
        booking = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=7)), ora=dt.time(hour=8))
        formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password', is_staff=True)
        booking_status = BookingStatus.objects.create(booking=booking, formatore=formatore, stato='1')

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertNotContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertNotContains(response, "Nessuna videolezione")
        self.assertContains(response, "Videolezioni live prenotate")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertNotContains(response, "Prenotazioni passate")

        #controllo sulle liste del context
        self.assertQuerysetEqual(response.context['booking'], [])
        booking_status_list = ['<BookingStatus: ' + booking_status.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_status'], booking_status_list)
        self.assertQuerysetEqual(response.context['booking_past'], [])

    def test_no_booking_no_bookingStatus_yes_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - non ci siano prenotazioni in attesa di conferma/annullamento
                - non ci siano prenotazioni già confermate/annullate per il futuro
                - ci siano prenotazioni già confermate/annullate per il passato
            (cioè le uniche prenotazioni fatte dall'utente sono state confermate/annullate
            e hanno una data passata rispetto ad oggi)
        '''
        #popolazione db per effettuare il test
        booking = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=-7)), ora=dt.time(hour=8))
        formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password', is_staff=True)
        booking_status = BookingStatus.objects.create(booking=booking, formatore=formatore, stato='1')

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertNotContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertContains(response, "Nessuna videolezione")
        self.assertNotContains(response, "Videolezioni live prenotate")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertContains(response, 'Prenotazioni passate')

        # controllo sulle liste del context
        self.assertQuerysetEqual(response.context['booking'], [])
        self.assertQuerysetEqual(response.context['booking_status'], [])
        booking_past_list = ['<BookingStatus: ' + booking_status.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_past'], booking_past_list)

    def test_yes_booking_no_bookingStatus_yes_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - ci siano prenotazioni in attesa di conferma/annullamento
                - non ci siano prenotazioni già confermate/annullate per il futuro
                - ci siano prenotazioni già confermate/annullate per il passato
            (cioè le prenotazioni fatte dall'utente o sono in attesa di conferma/annullamento
            o sono state confermate/annullate e hanno una data passata rispetto ad oggi)
        '''
        #popolazione db per effettuare il test
        booking_past = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=-7)), ora=dt.time(hour=8))
        booking = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=7)), ora=dt.time(hour=8))
        formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password', is_staff=True)
        booking_status = BookingStatus.objects.create(booking=booking_past, formatore=formatore, stato='1')

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertContains(response, "Nessuna videolezione")
        self.assertNotContains(response, "Videolezioni live prenotate")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertContains(response, 'Prenotazioni passate')

        # controllo sulle liste del context
        booking_list = ['<Booking: ' + booking.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking'], booking_list)
        self.assertQuerysetEqual(response.context['booking_status'], [])
        booking_past_list = ['<BookingStatus: ' + booking_status.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_past'], booking_past_list)

    def test_yes_booking_yes_bookingStatus_no_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - ci siano prenotazioni in attesa di conferma/annullamento
                - ci siano prenotazioni già confermate/annullate per il futuro
                - non ci siano prenotazioni già confermate/annullate per il passato
            (cioè le prenotazioni fatte dall'utente o sono in attesa di conferma/annullamento
            o sono state confermate/annullate e hanno una data futura rispetto ad oggi)
        '''
        #popolazione db per effettuare il test
        booking_future = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=17)), ora=dt.time(hour=8))
        booking = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=7)), ora=dt.time(hour=8))
        formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password', is_staff=True)
        booking_status = BookingStatus.objects.create(booking=booking_future, formatore=formatore, stato='1')

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertNotContains(response, "Nessuna videolezione")
        self.assertContains(response, "Videolezioni live prenotate")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertNotContains(response, 'Prenotazioni passate')

        # controllo sulle liste del context
        booking_list = ['<Booking: ' + booking.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking'], booking_list)
        booking_status_list = ['<BookingStatus: ' + booking_status.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_status'], booking_status_list)
        self.assertQuerysetEqual(response.context['booking_past'], [])

    def test_no_booking_yes_bookingStatus_yes_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - non ci siano prenotazioni in attesa di conferma/annullamento
                - ci siano prenotazioni già confermate/annullate per il futuro
                - ci siano prenotazioni già confermate/annullate per il passato
            (cioè le prenotazioni dell'utente, sia nel passato che nel futuro,
            sono state tutte confermate/annullate)
        '''
        #popolazione db per effettuare il test
        booking_future = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=7)), ora=dt.time(hour=8))
        booking_past = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=-7)), ora=dt.time(hour=8))
        formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password', is_staff=True)
        booking_status_future = BookingStatus.objects.create(booking=booking_future, formatore=formatore, stato='1')
        booking_status_past = BookingStatus.objects.create(booking=booking_past, formatore=formatore, stato='1')

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertNotContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertNotContains(response, "Nessuna videolezione")
        self.assertContains(response, "Videolezioni live prenotate")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertContains(response, 'Prenotazioni passate')

        # controllo sulle liste del context
        self.assertQuerysetEqual(response.context['booking'], [])
        booking_status_list = ['<BookingStatus: ' + booking_status_future.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_status'], booking_status_list)
        booking_past_list = ['<BookingStatus: ' + booking_status_past.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_past'], booking_past_list)

    def test_yes_booking_yes_bookingStatus_yes_bookingPast(self):
        '''
            controllo la view nel caso in cui:
                - ci siano prenotazioni in attesa di conferma/annullamento
                - ci siano prenotazioni già confermate/annullate per il futuro
                - ci siano prenotazioni già confermate/annullate per il passato
            (cioè l'utente ha effettuato prenotazioni che devono ancora essere confermate/annullate
            e quelle già confermate/annullate sono sia nel passato che nel futuro)
        '''
        #popolazione db per effettuare il test
        booking_future = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=7)), ora=dt.time(hour=8))
        booking_past = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=-7)), ora=dt.time(hour=8))
        booking = Booking.objects.create(user=self.user, data=(dt.date.today() + dt.timedelta(days=3)), ora=dt.time(hour=8))
        formatore = User.objects.create(username='formatore1', email='formatore@1.it', password='formatore1password', is_staff=True)
        booking_status_future = BookingStatus.objects.create(booking=booking_future, formatore=formatore, stato='1')
        booking_status_past = BookingStatus.objects.create(booking=booking_past, formatore=formatore, stato='1')

        #CONTROLLI
        response = self.client.get(reverse('user_booking'))
        self.assertEqual(response.status_code, 200)

        #controllo su prenotazioni non ancoraa confermate/annullate
        self.assertContains(response, 'Prenotazioni in attesa di conferma')
        #controllo su prenotazioni future già confermate/annullate
        self.assertNotContains(response, "Nessuna videolezione")
        self.assertContains(response, "Videolezioni live prenotate")
        #controllo su prenotazioni passate già confermate/annullate
        self.assertContains(response, 'Prenotazioni passate')

        # controllo sulle liste del context
        booking_list = ['<Booking: ' + booking.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking'], booking_list)
        booking_status_list = ['<BookingStatus: ' + booking_status_future.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_status'], booking_status_list)
        booking_past_list = ['<BookingStatus: ' + booking_status_past.__str__() + '>']
        self.assertQuerysetEqual(response.context['booking_past'], booking_past_list)

#test effettuati con un membro dello staff registrato e già loggato
class UserBookingView_StaffLogin_Test(TestCase):

    def setUp(self):
        '''
            istanzio un client,
            creo un membro dello staff nel database
            ed effettuo il login con questo membro dello staff appena creato
        '''
        self.client = Client()
        self.formatore = User.objects.create_user(username='formatore1', email='formatore@1.it', password='formatore1password')
        self.formatore.is_staff = True
        self.formatore.is_superuser = False
        self.formatore.is_active = True
        self.formatore.save()
        self.client.login(username='formatore1', password='formatore1password')
        self.assertTrue(self.client.login(username='formatore1', password='formatore1password'))

    def test_template(self):
        '''
            verifico che il template aperto sia quello corretto,
            cioè quello che mostra l'errore a fronte di un tentativo di accesso
            da parte di un membro dello staff ad una pagina a lui proibita
        '''

        #CONTROLLI
        response = self.client.get(reverse('user_booking'), follow=True)
        self.assertEqual(response.status_code, 200)

        #controllo di essere ridirezionato alla pagina con il template giusto
        self.assertTemplateNotUsed(response, 'user_management/user/user_booking.html')
        self.assertTemplateUsed(response, 'user_management/staff/staff_error.html')
        #controllo che il contenuto della pagina sia corretto (cioè il messaggio di errore per lo staff)
        self.assertContains(response, 'In qualità di membro dello staff non puoi accedere a questa pagina')

#test effettuati con un amministratore registrato e già loggato
class UserBookingView_AdminLogin_Test(TestCase):

    def setUp(self):
        '''
            istanzio un client,
            creo un membro dello staff nel database
            ed effettuo il login con questo membro dello staff appena creato
        '''
        self.client = Client()
        self.formatore = User.objects.create_user(username='formatore1', email='formatore@1.it', password='formatore1password')
        self.formatore.is_staff = True
        self.formatore.is_superuser = True
        self.formatore.is_active = True
        self.formatore.save()
        self.client.login(username='formatore1', password='formatore1password')
        self.assertTrue(self.client.login(username='formatore1', password='formatore1password'))

    def test_template(self):
        '''
            verifico che il template aperto sia quello corretto,
            cioè quello che mostra l'errore a fronte di un tentativo di accesso
            da parte di un membro dello staff ad una pagina a lui proibita
        '''

        #CONTROLLI
        response = self.client.get(reverse('user_booking'), follow=True)
        self.assertEqual(response.status_code, 200)

        #controllo di essere ridirezionato alla pagina con il template giusto
        self.assertTemplateNotUsed(response, 'user_management/user/user_booking.html')
        self.assertTemplateUsed(response, 'user_management/staff/staff_error.html')
        #controllo che il contenuto della pagina sia corretto (cioè il messaggio di errore per lo staff)
        self.assertContains(response, 'In qualità di membro dello staff non puoi accedere a questa pagina')