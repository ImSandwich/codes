<html>
    <head>
        <title>Page Attributes</title>
    </head>
    <body>
        <a href="page_attributes.php?action=A">Go to A</a>
        <a href="page_attributes.php?action=B">Go to B</a>
        <a href="page_attributes.php?action=C">Go to C</a>   
        <?php
        if (isset($_GET["action"]))
        {
            echo sprintf("<script>alert('You are viewing %1s ')</script>", $_GET["action"]);
        }
        ?>
    </body>
</html>