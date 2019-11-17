  <!DOCTYPE html>
  <html lang="en">

  <?php
    $host = 'db';
    $user = 'admin';
    $password = 'admin';
    $db = 'spotify_data';

    $conn = new mysqli($host, $user, $password, $db);
  ?>

  <head>
    <meta charset="utf-8">
    <title>Remember - Multipurpose bootstrap site template</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="description" content="Your page description here" />
    <meta name="author" content="" />

    <!-- css -->
    <link href="bigdata_webserver/css/bootstrap.css" rel="stylesheet" />
    <link href="bigdata_webserver/css/bootstrap-responsive.css" rel="stylesheet" />
    <link href="bigdata_webserver/css/prettyPhoto.css" rel="stylesheet" />
    <link href="https://fonts.googleapis.com/css?family=Open+Sans:300,400,600,700" rel="stylesheet">
    <link href="bigdata_webserver/css/style.css" rel="stylesheet">

    <!-- Theme skin -->
    <link id="t-colors" href="color/default.css" rel="stylesheet" />

    <!-- Fav and touch icons -->
    <link rel="apple-touch-icon-precomposed" sizes="144x144" href="bigdata_webserver/ico/apple-touch-icon-144-precomposed.png" />
    <link rel="apple-touch-icon-precomposed" sizes="114x114" href="bigdata_webserver/ico/apple-touch-icon-114-precomposed.png" />
    <link rel="apple-touch-icon-precomposed" sizes="72x72" href="bigdata_webserver/ico/apple-touch-icon-72-precomposed.png" />
    <link rel="apple-touch-icon-precomposed" href="bigdata_webserver/ico/apple-touch-icon-57-precomposed.png" />
    <link rel="shortcut icon" href="bigdata_webserver/ico/favicon.png" />
  </head>

  <body>
    <div id="wrapper">
      <!-- start header -->
      <header>
        <div class="top">
          <div class="container">
            <div class="row">
              
            </div>
          </div>
        </div>
        <div class="container">


          <div class="row nomargin">
            <div class="span6">
              <div class="logo">
                <h1><a href="index.html"><i class="icon-tint"></i> Spotify - Audioanalysis</a></h1>
              </div>
            </div>
          </div>
        </div>
      </header>
      <!-- end header -->

      <!-- section intro -->
      <section id="content">
        <div class="container">
          <h2>SPOTYFI: Music categorys from audio features</h2>
          <h3></h3>
        </div>
      </section>
      <!-- /section intro -->

      <section id="content">
        <div class="container">

          <div class="span12">
            <h4 class="heading">Hitradio: Das Beste von heute und die größten Hits der letzten Jahre.</h4>

            <table class="table table-striped">
              <thead>
                <tr>
                  <th>Id</th>
                  <th>Title</th>
                  <th>Künstler</th>
                  <th>Kategory</th>
                </tr>
              </thead>
              <tbody>
                <?php
                  $sql = 'SELECT * FROM titledata';
                  if($result = $conn->query($sql)) {
                    while($row = $result->fetch_row()) {
                      echo "<tr><td>" . $row[0] . "</td><td>" . $row[1] . "</td><td>" . $row[2] . "</td><td>" . $row[3] . "</td></tr>";
                    }
                  }
                ?>              
              </tbody>
            </table>
          </div>
          
        </div>
      </section>         
      <footer>
        <div class="container">
          <div class="row">
            <div class="span4">
              <div class="widget">
                <div class="footer_logo">
                  <h3><a href="index.html"><i class="icon-tint"></i> Spotify - Audioanalysis</a></h3>
                </div>
                <address>
                  <strong>BigData</strong><br>
                  DHBW Stuttgart<br>
                  70180 Stuttgart Deutschland
                </address>
                <p>
                  <i class="icon-phone"></i> (123) 456-7890 - (123) 555-7891 <br>
                  <i class="icon-envelope-alt"></i> bigdata@dhbw.com
                </p>
              </div>
            </div>         
          </div>
        </div>
        <div id="sub-footer">
          <div class="container">
            <div class="row">
              <div class="span6">
                <div class="copyright">
                  <p><span>&copy; Audioanalysis All right reserved</span></p>
                </div>
              </div>            
            </div>
          </div>
        </div>
      </footer>
    </div>
    <a href="#" class="scrollup"><i class="icon-angle-up icon-rounded icon-bglight icon-2x"></i></a>

    <!-- javascript
      ================================================== -->
    <!-- Placed at the end of the document so the pages load faster -->
    <script src="bigdata_webserver/js/jquery.js"></script>
    <script src="bigdata_webserver/js/jquery.easing.1.3.js"></script>
    <script src="bigdata_webserver/js/bootstrap.js"></script>
    <script src="bigdata_webserver/js/modernizr.custom.js"></script>
    <script src="bigdata_webserver/js/toucheffects.js"></script>
    <script src="bigdata_webserver/js/google-code-prettify/prettify.js"></script>
    <script src="bigdata_webserver/js/jquery.prettyPhoto.js"></script>
    <script src="bigdata_webserver/js/portfolio/jquery.quicksand.js"></script>
    <script src="bigdata_webserver/js/portfolio/setting.js"></script>
    <script src="bigdata_webserver/js/animate.js"></script>

    <!-- Template Custom JavaScript File -->
    <script src="jbigdata_webserver/s/custom.js"></script>

  </body>

  </html>
