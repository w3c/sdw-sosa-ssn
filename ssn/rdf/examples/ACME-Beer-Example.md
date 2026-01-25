# Tracking Beer Temperature with IBS-TH2 Sensor

An RDF file containing a [graph corresponding to this example is available](./rdf/examples/Beer-Full-IBS-TH2.ttl).

The following is a detailed example where a IBS-TH2 sensor is used to monitor a crate (carton) of beer from the time of its
packaging at a brewery up until its display in the supermarket cooler where it is purchased.  Beer degrades both
at high and low temperatures.  This requires it to be kept cool during storage and shipping to preserve the
product. Humidity has no effect on the beer, owing to sealed containers, though excess humidity will weaken cardboard and degrade
the adhesives, potentially resulting in product breakage.  Brewers will on occasion insert a temperature logger into
their shipping process as part of their quality control program. We present such a hypothetical situation here.

This example is of interest because it involves the repurposing of a
commodity, a consumer-grade [sosa:Platform](https://www.w3.org/TR/vocab-ssn/#SOSAPlatform)
deployed to address a domain-specific problem, the movement of a platform
from environment to environment and the possible ambiguity of data-ownership
in each of these environments.  It also demonstrates the location ambiguity
that can sometimes be present when modeling sensor readings.

Note: The use of long identifiers is for readability purposes and is non-normative.

## Packaging and initial storage
![InkBird_IBS_TH2-packaging](../../images/InkBird_IBS_TH2-packaging.png "The sensor platform and the beer are packaged into a container as a product")

Alice works for Acme Brewery Co. She procures an InkBird IBS-TH2 Platform (Serial Number: 12345) and places it inside a beer carton with six
bottles (a "six-pack") of Acme Brewery's famous Porter beers with a product lot code of PO202402. She seals the package and places it inside of Acme
Brewery's cooler to await shipment.

We model the packaging activity and the placement of the Platform into the
crate before it is sealed. The platform monitors the ambient air temperature and the relative humidity within
the beer crate every few minutes. In the following snippet, we instantiate the IBS-TH2 Platform, the carton, and the
activity that represents the packaging of the beer and the creation of the beer carton as a product:

The platform then begins to take measurements that are recorded as part of a data logging activity.

```
@prefix rdf:  <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>.
@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix qudt: <http://qudt.org/schema/qudt/> .
@prefix unit: <http://qudt.org/vocab/unit/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix schema: <http://schema.org/> .
@prefix gs1: <https://gs1.org/voc/> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rel: <http://id.loc.gov/vocabulary/relators/> .
@prefix sosa-env: <http://www.w3.org/ns/sosa/system-environment-properties#> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix geosparql: <http://www.opengis.net/ont/geosparql#> .
@prefix org: <http://www.w3.org/ns/org#> .
@prefix beer: <https://rdf.ag/o/beer#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix sosa: <http://www.w3.org/ns/sosa/> .
@prefix ex: <http://example.org/> .
@prefix sensor: <https://example.org/sensor/> .
@base <http://example.org/data/> .
#In this scenario a local brewery makes use of the sensor to track the 
#temperature of their beer as it is packaged, stored, shipped and displayed for sale.

<acmeBreweryCo> a org:Organization, beer:Brewery ;
	foaf:name "Acme Brewery Co." .

<acmeBrewerCooler> a ex:Cooler .

<alice> a foaf:Person, prov:Agent ;
	foaf:name "Alice" .

# A "six pack" as packaged and sold by Acme Brewery Co.

<acmePorterSixPack> a beer:Porter, gs1:Product, schema:Product ;
    skos:definition "A six pack of Acme Porter."@en .

# A specific (instance) six pack of Acme Porter Beers
# We use GS1-style lot and serial numbers as part of the 
# identifier to highlight that this is a physical instance of the product.
 
<10/PO202402/21/0001/acmePorterSixPack> a schema:IndividualProduct;
    rdfs:subClassOf <acmePorterSixPack>;
    gs1:packaging <0001/ProductPackaging>;
    gs1:hasBatchLotNumber "PO202402" ;
    gs1:hasSerialNumber "0001" .

<0001/ProductPackaging> a gs1:PackagingDetails, sosa:FeatureOfInterest ;  
    rdfs:label "An instance of a beer carton used to package a six pack."@en .

# Alice packages the Beer.

<12345/someTH2> a sensor:IBS-TH2-Plus, schema:IndividualProduct ;
    rel:own <acmeBreweryCo> ; # Sensor may be returned.
    rdfs:label "InkBird Sensor that Alice bought to track beer storage."@en ;
    sosa:hasSubSystem <12345/HumiditySensor>, <12345/TemperatureSensor> ;
    gs1:hasSerialNumber "12345" ;
    ex:deviceAddress "12:34:56:12:34:56" .

<00001/packingSixPack> a prov:Activity ;
    rdfs:comment "When Alice packaged Porter bottles into the box, she added an InkBird logger to check that the beer wasn't getting too warm in transit and storage." ;    
    prov:wasAssociatedWith <alice> ;
    prov:used <12345/someTH2> ;
    prov:used <0001/ProductPackaging> ;
    prov:startedAtTime "2024-02-20T01:35:00Z"^^xsd:dateTime;
    prov:endedAtTime   "2024-02-20T01:40:00Z"^^xsd:dateTime;   
    prov:atLocation <acmeBreweryCo> ;
    prov:generated <10/PO202402/21/0001/acmePorterSixPack> .

# These definitions look redundant; but they represent the specific, physical instantiation of the sensors.

<12345/HumiditySensor> a sensor:IBS-TH2-Plus-H ;
    rdf:comment "This is the instance of the humidity sensor instance."@en .

<12345/TemperatureSensor> a sensor:IBS-TH2-Plus-T ;
    rdf:comment "This is the instance of the temperature sensor instance."@en .
#
# Sensor activates and records temperature while in the brewery cooler.
    
<1a/observation> a sosa:Observation ;
    rel:own <acmeBreweryCo> ;
    sosa:observedProperty sosa-env:AmbientTemperature ;
    sosa:hasUltimateFeatureOfInterest <10/PO202402/21/0001/acmePorterSixPackBeerSample> ; 
    sosa:madeBySensor <12345/TemperatureSensor>  ;
    sosa:hasFeatureOfInterest <10/PO202402/21/0001/acmePorterSixPackAirSample> ;
    sosa:resultTime "2024-02-20T01:35:45Z"^^xsd:dateTime ;
    sosa:hasResult [
      a qudt:QuantityValue ;
      qudt:hasUnit unit:DEG_C ;
      qudt:value 12.0 ;
    ] ;
.
<1b/observation> rdf:type sosa:Observation ;
    rel:own <acmeBreweryCo> ;
    sosa:observedProperty sosa-env:AmbientHumidity;
    sosa:hasUltimateFeatureOfInterest <0001/ProductPackaging>;
    sosa:madeBySensor <12345/HumiditySensor>  ;
    sosa:hasFeatureOfInterest <10/PO202402/21/0001/acmePorterSixPackAirSample> ;
    sosa:resultTime "2024-02-20T01:35:45Z"^^xsd:dateTime ;
    sosa:hasResult [
      a qudt:QuantityValue ;
      qudt:hasUnit unit:PERCENT ;
      qudt:value 60 ;
    ] ;
.
<breweryObserver> a prov:Activity ;
    rdfs:comment "Brewery operating system logging process." ;
    prov:atLocation <acmeBreweryCo> ;
    prov:generated <1a/observation> ;
    prov:generated <1b/observation> ;
    prov:wasStartedBy <alice> . # She turned it on last time.     
```

   In the example above, concurrent use of the <a href="#SOSAhasFeatureOfInterest"><code>sosa:hasFeatureOfInterest</code></a> and <a
   href="#SOSAhasUltimateFeatureOfInterest"><code>sosa:hasUltimateFeatureOfInterest</code></a> properties is made to account for the repurposing of a generic
   sensor. The actual measurement performed by the platform is the air temperature within the carton, as a proxy for the beer
   temperature within each beer vessel. Modeling the full thermodynamic activity relating one measurement to the other is beyond the
   scope of this document, but could be implemented as a second order "virtual" <a href="#SOSASensor"><code>sosa:Sensor</code></a> or a
   sophisticated <a href="#SOSAProcedure"><code>sosa:Procedure</code></a>. Thus the use of the <a href="#SOSAhasUltimateFeatureOfInterest"><code>sosa:hasUltimateFeatureOfInterest</code></a> property allows for flexibility in interpretation of the measurement
   within a context <i>not necessarily intended by the original sensor design</i>.
   
   Physically, both <12345/HumiditySensor> and <12345/TemperatureSensor> are monitoring the ambient air within the
   specific Porter carton which we define as <10/PO202402/21/0001/acmePorterSixPackAirSample> which resolves the issue of the
   location of the measurement when the carton itself is in motion. The <a href="#SOSAhasUltimateFeatureOfInterest"><code>sosa:hasUltimateFeatureOfInterest</code></a> property
   targets the beer temperature within that carton and the humidity the cardboard of the carton was subjected to:

   <pre class="example turtle" data-include="./rdf/examples/Beer-FeatureOfInterest-IBS-TH2.ttl" data-include-format="text"></pre>

   The SOSA ontology takes a "feature and property" approach that is referenced by observations. The
   feature of interest &mdash; in this case, the ambient air within the carton
   (<10/PO202402/21/0001/acmePorterSixPackAirSample>) &mdash; is
   the feature that the Platform is concerned with. However, it is really a proxy for both the temperature of the beer within the
   individual containers (<10/PO202402/21/0001/acmePorterSixPackBeerSample>)
   within the carton and the relative humidity to which
   the packaging (<0001/ProductPackaging>) is being exposed. The beer "sample" in this case is virtual; the node
   serves only to semantically link the observation to the beer liquid itself without any physical sample being taken. A more
   detailed example with physical beer samples is found in [[[#beerCollections]]].
</div> 

## Shipping to Retail Store<

![InkBird_IBS_TH2-shipping](../../images/InkBird_IBS_TH2-shipping.png "The beer carton is moved from the brewery to the retail location.")

After being chilled in the brewery cooler, the beer carton is then loaded on one of the Acme delivery trucks for shipment to the retail store. The truck's cooling management system is recording the sensor readings for both the shipping company and the brewery. An on-board GPS unit annotates the activity of recording observations as the truck moves from location to location. This position information represents the location of the shipping truck itself without reference to the beer carton or the platform generating the readings. This is important, in that the underlying properties and features referenced by the sensors of the platform have not changed, even through the beer carton and the platform have obviously changed physical location.

The information recorded during this time period would be:

<pre class="example turtle" data-include="./rdf/examples/Beer-Shipping-IBS-TH2.ttl" data-include-format="text"></pre>
 
The sensors of the platform are reporting values for the same properties of the same features of interest; the physical location of the carton of beer does not effect the process because the platform monitors the inside of the carton itself. Modeling its location and the process of (un)loading of the carton from the truck is done through other rdf nodes. The truck on-board monitoring system does report a GPS geometry as a Location. This is the location at which the data was recorded from the platform. It is conceivable that the geometry node is shared with a vehicle tracking system rdf representation or the vehicle's delivery scheduling application but it is not mandated by Sosa. 

Note: Locations of Platform, Sensors, and measured samples are often conflated in non-semantically enabled systems and the semantics often implicitly assumed by the application. The deep semantic modeling within Sosa makes no such implicit assumptions and locations can be assigned to all elements independently.
 
## Display in Retail Store Cooler 

![InkBird_IBS_TH2-receiving](../../images/InkBird_IBS_TH2-receiving.png "The beer carton is stored in the display cooler for retail sale.")

When received from the delivery company by the retail store, the beer is displayed for sale in retail coolers which log the sensors to the data being held by the retail store. We notice again the semantics of location and containment; the sensor is contained within the carton, which is contained within the cooler, which is itself located within the store. However, none of these semantic is recorded. The only location activity is the activity is taking place within the supermarket cooler; not the supermarket itself. 

 </div>
 The information recorded during this time period would be:
 <pre class="example turtle" data-include="./rdf/examples/Beer-Supermarket-IBS-TH2.ttl" data-include-format="text"></pre>

 </div>

 ## Notes on deployment and observation aggregation
 
 In previous examples, <a href="https://www.w3.org/TR/prov-o/Activity">prov:Activity</a> was used as a means of aggregating
 results in an archiving reception. Other mechanisms exists to define the purpose of the System and to aggregate collections of
 results within specific contexts. 

 
 ### Recording data and sensor tasking through sensor deployments
 
 SOSA provides the notion of a <a href="#SOSADeployment">Deployment</a> class. This permits the tasking
 or installation of sensors to different environments, purposes, locations, or
 leases. Intended to link Platforms to Systems, it allows the application of different semantics to different situations,
 by recording different configuration parameters, for example, though deployments may be concurrent. Reusing the example of [[[#beerTemp]]], the sensor can be seen to be concurrently deployed within one
 beer carton and multiple coolers or storage sites:
 <pre class="example turtle" data-include="./rdf/examples/Beer-PlatformDeployment-IBS-TH2.ttl" data-include-format="text"></pre>
 
 ### Recording data using observation collection

 SOSA provides a lightweight capability to aggregate members for convenience. In previous examples, observations where
 clustered according to Deployment or recording Activity. In some circumstances, it is useful to aggregate observations
 according to an ad-hoc classification, here following the storage location of the carton while dispensing with geospatial
 data:
 
 <pre class="example turtle" data-include="./rdf/examples/Beer-ObservationCollections-IBS-TH2.ttl" data-include-format="text"></pre>

### Recording data using sample collection</h5> 


A similar class <a href="#SOSASampleCollection"><code>sosa:SampleCollection</code></a> allows for the aggregation of <a href="#SOSASample"><code>sosa:Samples</code></a>, for example as part of a collection of samples taken as part of a quality assurance program. In the case of Acme Brewery, a collection of beer samples could be represented in this manner:  

    <pre class="example turtle" data-include="./rdf/examples/Beer-SampleCollections-IBS-TH2.ttl" data-include-format="text"></pre>
    
Note: Thank you to Tudor Whiteley for the images. 
