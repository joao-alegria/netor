from api.controller import app
from rabbitmq.messaging import MessageReceiver
import db.persistance as persistance

if __name__ == '__main__':
    try:
        persistance.session.query(persistance.Domain).filter(persistance.Domain.domainId=="osm").first()
    except:
        domain=persistance.Domain(domainId="osm",admin="ITAV",description="test domain",auth=False,interfaceType="HTTP",url="10.0.12.118",name="osmTest",owner="joao")
        persistance.persist(domain)

    messageReceiver=MessageReceiver()
    messageReceiver.start()

    app.debug = True
    app.secret_key = 'tenantManager'
    app.run(port=5001)