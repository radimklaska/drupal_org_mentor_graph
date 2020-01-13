# Drupal.org Mentor graph

Loads mentors using drupal.org API and visualizes the result using graphviz.

![radimklaska mentor graph](./examples/229127_radimklaska_depth_10/229127_radimklaska_depth_3.png)
See the examples folder for more depth options. It gets a bit crazy after 4. :-) 

## Requirements

* Python3 to run the code
* graphviz
    * `sudo apt install graphviz` or `brew install graphviz`

## How to run the program

```bash
python3 do_mentors_graph.py --user 229127 --depth 2
```

The `--user` argument is mandatory, the `--depth` argument is optional and
defaults to 3.

## How this works

Uses drupal.org API: https://www.drupal.org/drupalorg/docs/apis/rest-and-other-apis