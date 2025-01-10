"""Flask SQLAlchemy ORM models for Social Auth"""

from mongoengine import ReferenceField
from social_core.utils import module_member, setting_name
from social_mongoengine.storage import (
    BaseMongoengineStorage,
    MongoengineAssociationMixin,
    MongoengineCodeMixin,
    MongoengineNonceMixin,
    MongoenginePartialMixin,
    MongoengineUserMixin,
)


class FlaskStorage(BaseMongoengineStorage):
    user = None
    nonce = None
    association = None
    code = None
    partial = None


def init_social(app, db):
    User = module_member(app.config[setting_name("USER_MODEL")])

    class UserSocialAuth(db.Document, MongoengineUserMixin):
        """Social Auth association model"""

        user = ReferenceField(User)

        @classmethod
        def user_model(cls):
            return User

    class Nonce(db.Document, MongoengineNonceMixin):
        """One use numbers"""

    class Association(db.Document, MongoengineAssociationMixin):
        """OpenId account association"""

    class Code(db.Document, MongoengineCodeMixin):
        """Mail validation single one time use code"""

    class Partial(db.Document, MongoenginePartialMixin):
        """Partial pipeline storage"""

    # Set the references in the storage class
    FlaskStorage.user = UserSocialAuth
    FlaskStorage.nonce = Nonce
    FlaskStorage.association = Association
    FlaskStorage.code = Code
    FlaskStorage.partial = Partial
