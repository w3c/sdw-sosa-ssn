# Informative Examples

## Product temperature and humidity monitoring

This section is a series of examples that represent a IBS-TH2 sensor.  At the
time of this publication it is a commercially available consumer grade
temperature and humidity sensor.  The sensor is modeled here as a 
[sosa:Platform](http://www.w3.org/ns/sosa/Platform)
that [sosa:hosts](http://www.w3.org/ns/sosa/hosts) three different
[sosa:Sensor](http://www.w3.org/ns/sosa/Sensor)s, one measuring air temperature,
another air relative humidity and a third for battery health.

The sensors have operating limits and accuracies that are described in the
litterature of the manufacturer.  These values are represented within the
ontology for querying as nominal platform values.  Importantly, the primary
source for these operating values, the manufacturer's litterature, is directly
referenced in the [sosa:Procedure](http://www.w3.org/ns/sosa/Procedure) node of
the description as a means of providing full documentation for the sensor.

The result is a complete ontological description of the IBS-TH2 sensor using
the core SSN ontology.  As this represents the ontological concept of the
product, all nodes are subClasses of the sosa Classes that are meant to be
instantiated for individual sensors.

An ontological representation is located in file InkBird-IBS-TH2.ttl

### Device Instantiation

A simple instantiation of a sensor would be:

```
_:anInkBirdSensor a equipment:InkBird-IBS-TH2 ;
    rdfs:label "InkBird Sensor that Bob bought."@en ;
    sosa:hosts _:BatterySensorInstance, _:HumiditySensorInstance, _:TemperatureSensorInstance ;
    gs1:hasSerialNumber "9885" ;
    equipment:deviceAddress "12:34:56:12:34:56" .
```

Note that because the IBS-TH2 is instantiated, so are all of the hosted
[sosa:Sensor](http://www.w3.org/ns/sosa/Sensor)s on the
[sosa:Platform](http://www.w3.org/ns/sosa/Platform).  While this seems intially
redudant, these instances represent the physical sensors on the products as
well as the idiosyncrasies that apply to them due to manufacturing variance,
defects or outright wear and tear.  This makes it possible to record device
level innacuracies, limits as well as the specific batteries that were placed
into which device at what time.


