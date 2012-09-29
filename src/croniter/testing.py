from plone.testing.layer import Layer as Base

class Layer(Base):

    defaultBases = tuple()

class IntegrationLayer(Layer):
    """."""

class FunctionnalLayer(IntegrationLayer):
    """."""
                                  

CRONITER_FIXTURE = Layer()
CRONITER_INTEGRATION_TESTING = IntegrationLayer()
CRONITER_FUNCTIONAL_TESTING = FunctionnalLayer()
