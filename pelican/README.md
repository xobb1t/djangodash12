Pelican-powered blog
====================

  1. Install [Pelican](http://docs.getpelican.com/): ``pip install -r requirements.txt``
  2. Apply theme: ``make install_theme``
  3. Generate blog: ``pelican content -s pelicanconf.py``
  4. Update gh-pages branch: ``ghp-import output``
  5. Upload on GitHub: ``git push origin gh-pages``
  6. [Setting up a custom domain](https://help.github.com/articles/setting-up-a-custom-domain-with-pages)
