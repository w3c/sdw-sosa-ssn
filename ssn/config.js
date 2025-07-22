var respecConfig = {
  specStatus: "ED",
  shortName: "vocab-ssn-2023",
  //publishDate:  "2025-08-01",
  prevRecShortname: "vocab-ssn",
  previousPublishDate: "2017-10-19",
  previousMaturity: "TR",
  repoURL: "https://github.com/w3c/sdw-sosa-ssn/",
  edDraftURI: "https://w3c.github.io/sdw-sosa-ssn/ssn/",
  group: "wg/sdw",
  wgPublicList: "public-sdw-comments",
  implementationReportURI: "https://w3c.github.io/sdw-sosa-ssn/ssn-usage/",
  inlineCSS: true,
  noIDLIn: true,
  noLegacyStyle: false,
  noRecTrack: false,
  logos: [
    {
      src: "https://raw.githubusercontent.com/w3c/sdw-sosa-ssn/gh-pages/ssn/images/OGC-0.png",
      alt: "OGC",
      height: "70",
      width: "62",
      url: "https://www.ogc.org/"
    }
  ],
  editors: [
    {
      name: "Simon J D Cox",
      company: "Timely Logic, AU",
      note: "formerly CSIRO and OGC",
      orcid: "0000-0002-3884-3420",
      w3cid: 1796
    },
    {
      name: "Maxime Lefrançois",
      company: "École Nationale Supérieure des Mines de Saint-Étienne, FR",
      companyURL: "https://www.mines-stetienne.fr/",
      orcid: "0000-0001-9814-8991"
    },
    {
      name: "Rob Warren",
      company: "Glengarry Agriculture and Farming, CA",
      companyURL: "https://github.com/GlengarryAg"
    },
    {
      name: "Luis Moreira de Sousa",
      company: "Instituto Superior Técnico Lisboa, PT",
      companyURL: "https://tecnico.ulisboa.pt/en/",
      orcid: "0000-0002-5851-2071"
    },
    {
      name: "Rob Atkinson",
      company: "Metalinkage",
      orcid: "0000-0002-7815-2472"
    },
    {
      name: "Sylvain Grellet",
      company: "BRGM",
      companyURL: "https://brgm.fr/",
      orcid: "0000-0001-7656-1830"
    },
    {
      name: "Kathi Schleidt",
      company: "Datacove",
      companyURL: "https://www.datacove.eu/",
      orcid: "0000-0002-8011-7350"
    }
  ],
  formerEditors: [
    {
      name: "Armin Haller",
      company: "Australian National University, AU",
      companyURL: "https://www.cbe.anu.edu.au/",
      orcid: "0000-0003-3425-0780"
    },
    {
      name: "Krzysztof Janowicz",
      company: "Universität Wien, AT",
      companyURL: "https://www.univie.ac.at/",
      orcid: "0009-0003-1968-887X"
    },
    {
      name: "Danh Le Phuoc",
      company: "Technical University of Berlin, DE",
      companyURL: "http://www.tu-berlin.de/",
      orcid: "0000-0003-2480-9261"
    },
    {
      name: "Kerry Taylor",
      company: "Australian National University, AU",
      companyURL: "https://cecs.anu.edu.au/",
      orcid: "0000-0003-2447-1088"
    }
  ],
  otherLinks: [
    {
      key: "Contributors (ordered alphabetically by surname)",
      data: [
        {
          value: "Krzysztof Janowicz, Universität Wien, AT"
        }, {
          value: "Alex Robin, Georobotix, FR"
        }, {
          value: "Hylke van der Schaaf, Fraunhofer IOSB, DE"
        }
      ]
    },
    {
      key: "Previous Contributors (ordered alphabetically by surname)",
      data: [
        {
          value: "Raúl García-Castro, Universidad Politécnica de Madrid, ES"
        }, {
          value: "Joshua Lieberman, Tumbling Walls, US"
        }, {
          value: "Claus Stadler, Universität Leipzig, DE"
        }
      ]
    },
    {
      key: "OGC Document Number",
      data: [
        {
          value: "OGC 25-022"
        }
      ]
    }
  ],
  localBiblio: {
    "Lefrancois-et-al-2017": {
      href: "https://w3id.org/seas/SEAS-D2_2-SEAS-Knowledge-Model.pdf",
      authors: ["Maxime Lefrançois", "Jarmo Kalaoja", "Takoua Ghariani", "Antoine Zimmermann"],
      title: "The SEAS Knowledge Model",
      status: "Deliverable 2.2",
      publisher: "ITEA2 12004 Smart Energy Aware Systems",
      date: "2017"
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
    "Project-PROV": {
      href: "https://linked.data.gov.au/def/project/",
      authors: ["Simon J D Cox"],
      title: "A Project Ontology",
      date: "2017"
    },
    "SSN-PROV": {
      href: "http://ceur-ws.org/Vol-1401/paper-05.pdf",
      title: "Sensor Data Provenance: SSNO and PROV-O Together at Last",
      date: "2014",
      authors: ["Michael Compton", "David Corsar", "Kerry Taylor"],
      publisher: "CEUR: 7th International Conference on Semantic Sensor Networks"
    },
    "SSNX-Paper": {
      authors: ["Michael Compton", "Payam Barnaghi", "Luis Bermudez", "Raúl García-Castro", "Oscar Corcho", "Simon Cox", "John Graybeal", "Manfred Hauswirth", "Cory Henson", "Arthur Herzog", "Vincent Huang", "Krzysztof Janowicz", "W. David Kelsey", "Danh Le Phuoc", "Laurent Lefort", "Myriam Leggieri", "Holger Neuhaus", "Andriy Nikolov", "Kevin Page", "Alexandre Passant", "Amit Sheth", "Kerry Taylor"],
      title: "The SSN ontology of the W3C semantic sensor network incubator group",
      href: "http://www.sciencedirect.com/science/article/pii/S1570826812000571",
      publisher: "Web Semantics: Science, Services and Agents on the World Wide Web, 17:25-32 ",
      date: "December 2012"
    },
    "SSO-Pattern": {
      href: "http://ceur-ws.org/Vol-668/paper12.pdf",
      authors: ["Krzysztof Janowicz", "Michael Compton"],
      title: "The Stimulus-Sensor-Observation Ontology Design Pattern and its Integration into the Semantic Sensor Network Ontology",
      publisher: "CEUR: Proceedings of the 3rd International Workshop on Semantic Sensor Networks (SSN10)",
      date: "2010"
    },
    "SWE": {
      href: "https://www.ogc.org/about-ogc/domains/swe/",
      title: "Sensor Web Enablement (SWE)",
      publisher: "Open Geospatial Consortium"
    }
  }
}