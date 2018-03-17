<?php 

    if (!empty($_FILES['file']))
    {
        foreach($_FILES['file']['name'] as $key=>$name)
        {
            if ($_FILES['file']['error'][$key]==0 && move_uploaded_file($_FILES['file']['tmp_name'][$key], "files/{$name}"))
            {
                $uploaded[] = $name;

                
            }
        }
        //print_r($uploaded);
        $pyscript = "C:\wamp64\www\STTSS-transcript\scratchpad\python_file.py";
        $python = "C:\Python27\python.exe";
        
        exec("$python $pyscript $uploaded[0]", $output, $return);
        echo $output[0];

    }

            
            
            
?>
<html>
    <head>
        <title>Python Interface</title>
        <!-- <script type="text/javascript" src="python_interface.js"> </script> -->
    </head>
    <body>
        <p>Warning: This is work in progress!</p>
        <div id="uploaded">

        </div>
        <div id="upload_progress"></div>
        <div>
            <form enctype="multipart/form-data" action="" method="post">
                <div>
                    <input name="file[]" type="file" multiple="multiple"><br>
                    <input type="submit" value="Upload">
                </div>
            </form>
        </div>

    </body>
</html>
