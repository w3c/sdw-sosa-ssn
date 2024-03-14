var respecConfig = {
  specStatus: "ED",
  shortName: "vocab-ssn",
  //publishDate:  "2015-05-18",
  //previousPublishDate: "2014-03-27",
  //previousMaturity: "FPWD",
  //previousURI: "http://www.w3.org/TR/2014/WD-tabular-data-model-20140327/",
  edDraftURI: "https://w3c.github.io/sdw-sosa-ssn/ssn/",
  // lcEnd: "3000-01-01",
  // crEnd: "3000-01-01",
  editors: [
    {
      name: "Simon J D Cox",
      company: "OGC",
      companyURL: "https://ogc.org/",
      orcid: "0000-0002-3884-3420"
    },
    {
      name: "Maxime Lefrançois",
      company: "École Nationale Supérieure des Mines de Saint-Étienne",
      companyURL: "https://www.mines-stetienne.fr/",
      orcid: "0000-0001-9814-8991"
    },
    {
      name: "Krzysztof Janowicz",
      company: "Universität Wien",
      companyURL: "https://www.univie.ac.at/",
      orcid: "0009-0003-1968-887X"
    },
    {
      name: "Armin Haller",
      company: "Australian National University",
      companyURL: "https://www.cbe.anu.edu.au/"
    },
    {
      name: "Danh Le Phuoc",
      company: "Technical University of Berlin",
      companyURL: "http://www.tu-berlin.de/"
    },
    {
      name: "Kerry Taylor",
      company: "Australian National University",
      companyURL: "https://cecs.anu.edu.au/"
    }],
  otherLinks: [
    {
      key: "Contributors (ordered alphabetically)",
      data: [
        {
          value: "Rob Atkinson, Metalinkage"
        }, {
          value: "Luis de Sousa, ISRIC"
        }, {
          value: "Sylvan Grellet, BRGM"
        }, {
          value: "Kathi Schleidt, Datacove"
        }, {
          value: "Hylke van der Schaaf, Fraunhofer IOSB"
        }]
    },
    {
      key: "Previous Contributors (ordered alphabetically)",
      data: [
        {
          value: "Raúl García-Castro, Universidad Politécnica de Madrid"
        }, {
          value: "Joshua Lieberman, Tumbling Walls"
        }, {
          value: "Claus Stadler, Universität Leipzig"
        }]
    },
    {
      key: "OGC Document Number",
      data: [
        {
          value: "OGC NN-NNN"
        }]
    }],
  wg: "Spatial Data on the Web Working Group",
  wgURI: "https://www.w3.org/2015/spatial/",
  wgPublicList: "public-sdw-comments",
  wgPatentURI: "https://www.w3.org/2004/01/pp-impl/75471/status",
  implementationReportURI: "https://w3c.github.io/sdw/ssn-usage/",
  inlineCSS: true,
  noIDLIn: true,
  noLegacyStyle: false,
  logos: [
    {
      src: "https://www.w3.org/StyleSheets/TR/2016/logos/W3C",
      alt: "W3C",
      height: "48",
      width: "72",
      url: "https://www.w3.org/"
    },
    {
      src: "https://www.w3.org/2017/01/ogc_logo.png",
      alt: "OGC",
      height: "68",
      width: "147",
      url: "http://www.opengeospatial.org/"
    }
  ],
  noRecTrack: false,

  localBiblio: {
    "CDT": {
      href: "https://w3id.org/lindt/v4/custom_datatypes",
      title: "Custom Datatypes - Towards a web of Linked Datatypes",
      authors: ["Maxime Lefrançois", "Antoine Zimmermann"],
      date: "19 July 2021"
    },
    "GeoSPARQL": {
      href: "https://docs.ogc.org/is/22-047r1/22-047r1.html",
      title: "GeoSPARQL - A Geographic Query Language for RDF Data v1.1",
      authors: ["Nicholas J Car", "Timo Homburg", "Matthew Perry", "Frans Knibbe", "Simon J.D. Cox", "Joseph Abhayaratna", "Mathias Bonduel", "Paul J. Cripps", "Krzysztof Janowicz"],
      date: "29 January 2024"
    },
    "OandM": {
      href: "https://portal.ogc.org/files/?artifact_id=41579",
      title: "Observations and Measurements (O&M) v2",
      authors: ["Simon Cox"],
      publisher: "Open Geospatial Consortium",
      date: "2011"
    },
    "OBOE": {
      href: "http://dx.doi.org/10.5063/F11C1TTM",
      date: "2016",
      authors: ["Mark Schildhauer", "Matthew B. Jones", "Shawn Bowers", "Joshua Madin", "Sergeui Krivov", "Deana Pennington", "Ferdinando Villa", "Benjamin Leinfelder", "Christopher Jones", "Margaret O'Brien"],
      title: "OBOE: the Extensible Observation Ontology, version 1.1"
    },
    "OMS": {
      href: "https://docs.ogc.org/as/20-082r4/20-082r4.html",
      title: "Observations, measurements and samples (OMS)",
      authors: ["Katharina Schleidt", "Ilkka Rinne"],
      publisher: "Open Geospatial Consortium",
      date: "2023"
    },
    "SAREF_Patterns": {
      href: "https://www.etsi.org/deliver/etsi_ts/103500_103599/103548/01.02.01_60/ts_103548v010201p.pdf",
      title: "SmartM2M; SAREF reference ontology patterns",
      id: "ETSI TS 103 548 ",
      publisher: "ETSI",
      date: "2024"
    },
    "SAREF": {
      href: "https://www.etsi.org/deliver/etsi_ts/103200_103299/103264/03.02.01_60/ts_103264v030201p.pdf",
      title: "SmartM2M; Smart Applications; Reference Ontology and oneM2M Mapping",
      id: "ETSI TS 103 264 (V3.2.1)",
      publisher: "ETSI",
      date: "2024"
    },
    "SmartM2M": {
      href: "https://www.etsi.org/deliver/etsi_ts/103500_103599/103548/01.02.01_60/ts_103548v010201p.pdf",
      title: "SmartM2M; Smart Applications; Reference Ontology and oneM2M Mapping",
      id: "ETSI TS 103 264 (V3.2.1)",
      publisher: "ETSI",
      date: "2024"
    },
    "SensorML": {
      href: "https://www.ogc.org/standard/sensorml/",
      title: "Sensor Model Language (SensorML)",
      authors: ["Mike Botts", "Alexandre Robin"],
      publisher: "Open Geospatial Consortium",
      date: "2010"
    },
    "SWE": {
      href: "https://www.ogc.org/about-ogc/domains/swe/",
      title: "Sensor Web Enablement (SWE)",
      publisher: "Open Geospatial Consortium"
    },
    "STA": {
      href: "https://www.ogc.org/standard/sensorthings/",
      title: "OGC SensorThings API (STA)",
      publisher: "Open Geospatial Consortium"
    },
    "SSNX": {
      authors: ["Michael Compton", "Payam Barnaghi", "Luis Bermudez", "Raúl García-Castro", "Oscar Corcho", "Simon Cox", "John Graybeal", "Manfred Hauswirth", "Cory Henson", "Arthur Herzog", "Vincent Huang", "Krzysztof Janowicz", "W. David Kelsey", "Danh Le Phuoc", "Laurent Lefort", "Myriam Leggieri", "Holger Neuhaus", "Andriy Nikolov", "Kevin Page", "Alexandre Passant", "Amit Sheth", "Kerry Taylor"],
      title: "The SSN ontology of the W3C semantic sensor network incubator group",
      href: "http://www.sciencedirect.com/science/article/pii/S1570826812000571",
      publisher: "Web Semantics: Science, Services and Agents on the World Wide Web, 17:25-32 ",
      date: "December 2012"
    },
    "UCUM": {
      href: "https://ucum.org/ucum",
      title: "The Unified Code for Units of Measure",
      authors: ["Gunther Schadow", "Gunther Schadow"],
      publisher: "Regenstrief Institute, Inc.",
      date: "21 November 2017"
    },
    "DUL": {
      href: "http://ontologydesignpatterns.org/wiki/Ontology:DOLCE+DnS_Ultralite",
      authors: ["Aldo Gangemi"],
      title: "DOLCE+DnS Ultralite (DUL)"
    },
    "Cuenca-Grau-et-al-2009": {
      href: "https://www.cs.ox.ac.uk/publications/publication779-abstract.html",
      authors: ["Bernardo Cuenca Grau", "Ian Horrocks", "Yevgeny Kazakov ", "Ulrike Sattler"],
      title: "Extracting Modules from Ontologies: A Logic−based Approach",
      publisher: "Springer",
      date: "2009"
    },
    "SSO-Pattern": {
      href: "http://ceur-ws.org/Vol-668/paper12.pdf",
      authors: ["Krzysztof Janowicz", "Michael Compton"],
      title: "The Stimulus-Sensor-Observation Ontology Design Pattern and its Integration into the Semantic Sensor Network Ontology",
      publisher: "CEUR: Proceedings of the 3rd International Workshop on Semantic Sensor Networks (SSN10)",
      date: "2010"
    },
    "OBOE": {
      href: "http://dx.doi.org/10.5063/F11C1TTM",
      date: "2016",
      authors: ["Mark Schildhauer", "Matthew B. Jones", "Shawn Bowers", "Joshua Madin", "Sergeui Krivov", "Deana Pennington", "Ferdinando Villa", "Benjamin Leinfelder", "Christopher Jones", "Margaret O'Brien"],
      title: "OBOE: the Extensible Observation Ontology, version 1.1"
    },
    "OM-Heavy": {
      href: "http://ceur-ws.org/Vol-1063/paper1.pdf",
      title: "An explicit OWL representation of ISO/OGC Observations and Measurements ",
      publisher: "CEUR: 6th International Conference on Semantic Sensor Networks",
      date: "2013",
      authors: ["S.J.D. Cox"]
    },
    "OM-Lite": {
      href: "http://content.iospress.com/articles/semantic-web/sw214",
      doi: "10.3233/SW-160214",
      title: "Ontology for observations and sampling features, with alignments to existing models",
      publisher: "Semantic Web",
      date: "2017",
      volume: "8",
      page: "453-470",
      authors: ["S.J.D. Cox"]
    },
    "OMXML": {
      href: "http://portal.opengeospatial.org/files/41510",
      title: "Observations and Measurements - XML Implementation",
      publisher: "Open Geospatial Consortium",
      date: "2010",
      authors: ["S.J.D. Cox"]
    },
    "ISO-19150-2": {
      href: "https://www.iso.org/standard/57466.html",
      title: "Geographic information -- Ontology -- Part 2: Rules for developing ontologies in the Web Ontology Language (OWL)",
      publisher: "ISO",
      date: "July 2015"
    },
    "ISO-19109": {
      href: "https://www.iso.org/standard/59193.html",
      title: "Geographic information -- Rules for application schema",
      publisher: "ISO",
      date: "December 2015"
    },
    "ISO-19156": {
      href: "https://www.iso.org/standard/32574.html",
      title: "Geographic information -- Observations and measurements",
      publisher: "ISO",
      date: "December 2011"
    },
    "SensorML": {
      href: "http://portal.opengeospatial.org/files/55939",
      publisher: "OGC",
      title: "SensorML: Model and XML Encoding Standard 2.0",
      authors: ["Mike Botts", "Alex Robin"],
      status: "Encoding Standard, OGC 12-000",
      date: "2014"
    },
    "SSN-PROV": {
      href: "http://ceur-ws.org/Vol-1401/paper-05.pdf",
      title: "Sensor Data Provenance: SSNO and PROV-O Together at Last",
      date: "2014",
      authors: ["Michael Compton", "David Corsar", "Kerry Taylor"],
      publisher: "CEUR: 7th International Conference on Semantic Sensor Networks"
    },
    "SSN-Short": {
      authors: ["Kerry Taylor", "Michael Compton", "Laurent Lefort"],
      href: "https://eresearchau.files.wordpress.com/2012/06/74-semantically-enabling-the-web-of-things-the-w3c-semantic-sensor-network-ontology.pdf",
      title: "The Web of Things: The W3C Semantic Sensor Network Ontology",
      publisher: "5th Australasian eResearch Conference, Melbourne",
      date: "November 2011"
    },
    "Lefrancois-et-al-2017": {
      href: "https://w3id.org/seas/SEAS-D2_2-SEAS-Knowledge-Model.pdf",
      authors: ["Maxime Lefrançois", "Jarmo Kalaoja", "Takoua Ghariani", "Antoine Zimmermann"],
      title: "The SEAS Knowledge Model",
      status: "Deliverable 2.2",
      publisher: "ITEA2 12004 Smart Energy Aware Systems",
      date: "2017"
    },
    "Rijgersberg-et-al-2013": {
      href: "http://www.semantic-web-journal.net/content/ontology-units-measure-and-related-concepts",
      authors: ["Hajo Rijgersberg", "Mark van Assem", "Jan Top"],
      title: "Ontology of Units of Measure and Related Concepts",
      publisher: "Semantic Web journal, IOS Press",
      date: "2013"
    }
  },
  issueBase: "https://www.w3.org/2015/spatial/track/issues/"
};
