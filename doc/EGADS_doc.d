# vim: ft=make
.PHONY: EGADS_doc._graphics
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/base/makeidx.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/base/report.cls
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/base/textcomp.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/fancyhdr/fancyhdr.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/fancyvrb/fancyvrb.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/graphics/color.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/graphics/graphics.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/graphics/graphicx.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/graphics/keyval.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/graphics/trig.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/hyperref/hyperref.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/hyperref/nameref.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/listings/listings.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/listings/lstlang1.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/listings/lstmisc.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/listings/lstpatch.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/ltxmisc/url.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/oberdiek/kvoptions.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/oberdiek/refcount.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/paralist/paralist.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: /usr/share/texmf/tex/latex/tools/calc.sty
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: EGADS_doc.tex
EGADS_doc.aux EGADS_doc.aux.make EGADS_doc.d EGADS_doc.pdf: cover/doc_cover.tex
.SECONDEXPANSION:
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
-include cover/eufar_a_sm.pdf.gpi.d
EGADS_doc.d: $$(call graphics-source,cover/eufar_a_sm.pdf)
EGADS_doc.pdf EGADS_doc._graphics: $$(call graphics-target,cover/eufar_a_sm.pdf)
