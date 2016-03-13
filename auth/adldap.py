from django.conf import settings
from django.contrib.auth.models import User, check_password
import ldap

class ADLDAPBackend:
    
    def authenticate(self, username=None, password=None):

        session = self.ldap_bind(username, password)
        if not session:
            return None

        try:
            username2 = self.canonize_username(username)
            user = User.objects.get(username=username2)
        except User.DoesNotExist:
            if settings.AUTH_AD_CREATEUSER:
                user = self.create_user(session, username)
            else:
                user = None

        session.unbind()
        print "user=",user
        return user

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def canonize_username(self, name):
        return name.replace(' ', '_').lower()
  

    def ldap_bind(self, user, passwd):
        bind_name  = user + '@' + settings.AUTH_AD_DOMAIN
        server_uri = 'ldap://%s:%s' % (settings.AUTH_AD_SERVER, 
                                   settings.AUTH_AD_PORT)
        try:
            if settings.AUTH_AD_USETLS:
                # ldap.set_option(ldap.OPT_DEBUG_LEVEL,255)
                ldap.set_option(ldap.OPT_X_TLS_CACERTFILE, settings.AUTH_AD_CACERTFILE)
            ldap.set_option(ldap.OPT_REFERRALS, 0)

            l = ldap.initialize(server_uri)
            l.protocol_version = ldap.VERSION3
                      
            if settings.AUTH_AD_USETLS:
                l.set_option(ldap.OPT_X_TLS,ldap.OPT_X_TLS_DEMAND)
                l.start_tls_s()

            l.simple_bind_s(bind_name,passwd)      

        except ldap.INVALID_CREDENTIALS, e:
            return None
        except ldap.LDAPError, e:
            return None
        return l

    def create_user(self, session, username):

        search_fields = [ 'mail', 'givenName', 'sn', 'sAMAccountName']

        filter = "sAMAccountName=%s" % username
        if settings.AUTH_AD_FILTER:
            filter = "(&(%s)(%s))" % (filter, settings.AUTH_AD_FILTER)

        resultset = session.search_ext_s(settings.AUTH_AD_SEARCHDN,
                                         ldap.SCOPE_SUBTREE, 
                                         filter,
                                         search_fields)
        if not resultset:
            return None
      
        if not resultset[0][0]:
            return None
      
        result = resultset[0][1]

        # First Name
        if result.has_key('givenName'):
            first_name = result['givenName'][0]
        else:
            first_name = None
          
        #Last Name (sn)
        if result.has_key('sn'):
            last_name = result['sn'][0]
        else:
            last_name = None

        # Email Address
        if result.has_key('mail'):
            email = result['mail'][0]
        else:
            email = None

        user = User(username   = self.canonize_username(username),
                    first_name = first_name,
                    last_name  = last_name,
                    email      = email)

        user.is_staff = False
        user.is_superuser = False
        user.set_password('')
        user.save()
        return user
