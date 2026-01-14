# Tracking Beer Temperature with IBS-TH2 Sensor

An RDF file containing a <a href="./rdf/examples/Beer-Full-IBS-TH2.ttl">graph corresponding to this example is available.

The following is a detailed example where a IBS-TH2 sensor is used to monitor a crate (carton) of beer from the time of its
packaging at a brewery up until its display in the supermarket cooler where it is purchased.  Beer degrades both
at high and low temperatures.  This requires it to be kept cool during storage and shipping to preserve the
product. Humidity has no effect on the beer, owing to sealed containers, though excess humidity will weaken cardboard and degrade
the adhesives, potentially resulting in product breakage.  Brewers will on occasion insert a temperature logger into
their shipping process as part of their quality control program. We present such a hypothetical situation here.

This example is of interest because it involves the repurposing of a
commodity, a consumer-grade <a href="#SOSAPlatform">sosa:Platform</a>
deployed to address a domain-specific problem, the movement of a platform
from environment to environment and the possible ambiguity of data-ownership
in each of these environments.  It also demonstrates the location ambiguity
that can sometimes be present when modeling sensor readings.

Note: The use of long identifiers is for readability purposes and is non-normative.


## Packaging and initial storage
<div>
<figure id="InkBird_IBS_TH2-packaging" style="float: right; max-width: 30%; height: auto;vertical-align: top;margin: -10% 15px 0px 15px;">
<img src="./images/InkBird_IBS_TH2-packaging.png"> 
 <figcaption>The sensor platform and the beer are packaged into a container as a product.</figcaption> 
</figure>

Alice works for Acme Brewery Co. She procures an InkBird IBS-TH2 Platform (Serial Number: 12345) and places it inside a beer carton with six
bottles (a &quot;six-pack&quot;) of Acme Brewery's famous Porter beers with a product lot code of PO202402. She seals the package and places it inside of Acme
Brewery's cooler to await shipment.

We model the packaging activity and the placement of the Platform into the
crate before it is sealed. The platform monitors the ambient air temperature and the relative humidity within
the beer crate every few minutes. In the following snippet, we instantiate the IBS-TH2 Platform, the carton, and the
activity that represents the packaging of the beer and the creation of the beer carton as a product:

The platform then begins to take measurements that are recorded as part of a data logging activity.

<pre class="example turtle" data-include="./rdf/examples/Beer-Packaging-IBS-TH2.ttl" data-include-format="text"></pre>

   In the example above, concurrent use of the <a href="#SOSAhasFeatureOfInterest"><code>sosa:hasFeatureOfInterest</code></a> and <a
   href="#SOSAhasUltimateFeatureOfInterest"><code>sosa:hasUltimateFeatureOfInterest</code></a> properties is made to account for the repurposing of a generic
   sensor. The actual measurement performed by the platform is the air temperature within the carton, as a proxy for the beer
   temperature within each beer vessel. Modeling the full thermodynamic activity relating one measurement to the other is beyond the
   scope of this document, but could be implemented as a second order &quot;virtual&quot; <a href="#SOSASensor"><code>sosa:Sensor</code></a> or a
   sophisticated <a href="#SOSAProcedure"><code>sosa:Procedure</code></a>. Thus the use of the <a href="#SOSAhasUltimateFeatureOfInterest"><code>sosa:hasUltimateFeatureOfInterest</code></a> property allows for flexibility in interpretation of the measurement
   within a context <i>not necessarily intended by the original sensor design</i>.
   
   Physically, both &lt;12345/HumiditySensor&gt; and &lt;12345/TemperatureSensor&gt; are monitoring the ambient air within the
   specific Porter carton which we define as <small>&lt;10/PO202402/21/0001/acmePorterSixPackAirSample&gt;</small> which resolves the issue of the
   location of the measurement when the carton itself is in motion. The <a href="#SOSAhasUltimateFeatureOfInterest"><code>sosa:hasUltimateFeatureOfInterest</code></a> property
   targets the beer temperature within that carton and the humidity the cardboard of the carton was subjected to:
   <pre class="example turtle" data-include="./rdf/examples/Beer-FeatureOfInterest-IBS-TH2.ttl" data-include-format="text"></pre>

   The SOSA ontology takes a &quot;feature and property&quot; approach that is referenced by observations. The
   feature of interest &mdash; in this case, the ambient air within the carton
   (<small>&lt;10/PO202402/21/0001/acmePorterSixPackAirSample&gt;</small>) &mdash; is
   the feature that the Platform is concerned with. However, it is really a proxy for both the temperature of the beer within the
   individual containers (<small>&lt;10/PO202402/21/0001/acmePorterSixPackBeerSample&gt;</small>)
   within the carton and the relative humidity to which
   the packaging (<small>&lt;0001/ProductPackaging&gt;</small>) is being exposed. The beer &quot;sample&quot; in this case is virtual; the node
   serves only to semantically link the observation to the beer liquid itself without any physical sample being taken. A more
   detailed example with physical beer samples is found in [[[#beerCollections]]].
</div> 

<h4>Shipping to Retail Store</h4>
<div>
 <figure id="InkBird_IBS_TH2-shipping" style="float: right; max-width: 30%; height: auto;vertical-align: top;margin: -10% 15px 0px 15px;">
 <img src="./images/InkBird_IBS_TH2-shipping.png"> 
 <figcaption>The beer carton is moved from the brewery to the retail location.</figcaption> 
 </figure> 
</div> 
 After being
chilled in the brewery cooler, the beer carton is then loaded on one of the Acme delivery trucks for shipment to the retail
store.  The truck's cooling management system is recording the sensor readings for both the shipping company and the brewery.
An on-board GPS unit annotates the activity of recording observations as the truck moves from location to location. This
position information represents the location of the shipping truck itself without reference to the beer carton or the
platform generating the readings. This is important, in that the underlying properties and features referenced by the sensors
of the platform have not changed, even
through the beer carton and the platform have obviously changed physical location.

The information recorded during this time period would be:
<pre class="example turtle" data-include="./rdf/examples/Beer-Shipping-IBS-TH2.ttl" data-include-format="text"></pre>
 
    The sensors of the platform are reporting values for the same properties of the same features of interest; the physical
    location of the carton of beer does not effect the process because the platform monitors the inside of the carton itself. Modeling
    its location and the process of (un)loading of the carton from the truck is done through other rdf nodes. 
    The truck on-board monitoring system does report a GPS geometry as a Location. This is the location at which the data was
    recorded from the platform. It is conceivable that the geometry node is shared with a vehicle tracking system rdf representation
    or the vehicle's delivery scheduling application but it is not mandated by Sosa. 

<p class="note">Locations of Platform, Sensors, and measured samples are often conflated in
non-semantically enabled systems and the semantics often implicitly assumed by the application. The deep semantic modeling
within Sosa makes no such implicit assumptions and locations can be assigned to all elements independently.
 
<h4>Display in Retail Store Cooler</h4> 
<p style="margin-bottom: 0.5cm">
<div>
 <figure id="InkBird_IBS_TH2-receiving" style="float: right; max-width: 30%; height: auto;vertical-align: top; margin: -10px 15px 0px 15px;">
 <img src="./images/InkBird_IBS_TH2-receiving.png"> 
 <figcaption>The beer carton is stored in the display cooler for retail sale.</figcaption> 
 </figure> 
 When received from the delivery company by the retail store, the beer is displayed for sale in retail coolers which log
 the sensors to the data being held by the retail store. We notice again the semantics of location and containment; the sensor is
 contained within the carton, which is contained within the cooler, which is itself located within the store. However, none of these
 semantic is recorded. The only location activity is 
 the activity is taking place within the supermarket cooler; not the supermarket itself. 
 </div>
 The information recorded during this time period would be:
 <pre class="example turtle" data-include="./rdf/examples/Beer-Supermarket-IBS-TH2.ttl" data-include-format="text"></pre>

 </div>

 <h4>Notes on deployment and observation aggregation</h4>
 
 In previous examples, <a href="https://www.w3.org/TR/prov-o/Activity">prov:Activity</a> was used as a means of aggregating
 results in an archiving reception. Other mechanisms exists to define the purpose of the System and to aggregate collections of
 results within specific contexts. 

 
 <h5>Recording data and sensor tasking through sensor deployments</h5>
 
 SOSA provides the notion of a <a href="#SOSADeployment">Deployment</a> class. This permits the tasking
 or installation of sensors to different environments, purposes, locations, or
 leases. Intended to link Platforms to Systems, it allows the application of different semantics to different situations,
 by recording different configuration parameters, for example, though deployments may be concurrent. Reusing the example of [[[#beerTemp]]], the sensor can be seen to be concurrently deployed within one
 beer carton and multiple coolers or storage sites:
 <pre class="example turtle" data-include="./rdf/examples/Beer-PlatformDeployment-IBS-TH2.ttl" data-include-format="text"></pre>
 
 <h5 id="beerCollections">Recording data using observation collection</h5>

 SOSA provides a lightweight capability to aggregate members for convenience. In previous examples, observations where
 clustered according to Deployment or recording Activity. In some circumstances, it is useful to aggregate observations
 according to an ad-hoc classification, here following the storage location of the carton while dispensing with geospatial
 data:
 
 <pre class="example turtle" data-include="./rdf/examples/Beer-ObservationCollections-IBS-TH2.ttl" data-include-format="text"></pre>
 <h5 id="beerSamples">Recording data using sample collection</h5> 
    A similar class &mdash; <a href="#SOSASampleCollection"><code>sosa:SampleCollection</code></a> &mdash; allows for the aggregation of <a
    href="#SOSASample"><code>sosa:Samples</code></a>, for example as part of a collection of samples taken as part of a
    quality assurance program. In the case of Acme Brewery, a collection of beer samples could be represented in this manner:  

    <pre class="example turtle" data-include="./rdf/examples/Beer-SampleCollections-IBS-TH2.ttl" data-include-format="text"></pre>
    
    <p class="note">Note: Thank you to Tudor Whiteley for the images. 
    </section>
