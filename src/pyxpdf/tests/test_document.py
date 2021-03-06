import unittest
from .common_imports import InitGlobalTextCase, PropertyTextCase, file_in_test_dir
from pyxpdf.pdf import Document
from pyxpdf.xpdf import Config, XPDFConfigError

# TODO: add tests for encodings


class DocumentTextCase(InitGlobalTextCase, PropertyTextCase):
    simple_file = "samples/simple1.pdf"
    dmca_pdf = "samples/nonfree/dmca.pdf"
    mandarin_pdf = 'samples/nonfree/mandarin.pdf'
    dmca_prop = {
        'num_pages': 18,
        'pdf_version': 1.4,
        'is_linearized': True,
        'ok_to_copy': True,
        'info()': {'Creator': 'C:My DocumentsSUMMARY6.WPD',
                   'CreationDate': 'D:00000101000000Z',
                   'Title': 'The Digital Millennium Copyright Act of 1998',
                   'Author': 'United States Copyright Office - jmf',
                   'Producer': 'Acrobat PDFWriter 3.02 for Windows',
                   'Keywords': 'digital millennium copyright act circumvention technological protection management information online service provider liability limitation computer maintenance competitiion repair ephemeral recording webcasting distance education study vessel hull',
                   'Subject': 'Copyright Office Summary of the DMCA',
                   'ModDate': "D:20011017180926-03'00'"}
    }

    def setUp(self):
        super().setUp()
        Config.text_encoding = 'utf-8'
        Config.text_eol = 'unix'
        with open(file_in_test_dir('dcma_xmp.xml'), 'r', encoding='utf-8') as fp:
            self.dmca_prop['xmp_metadata()'] = fp.read()

    def _test_doc_properties(self, doc):
        for prop, value in self.dmca_prop.items():
            if '()' in prop:
                self.assertEqual(getattr(doc, prop.rstrip('()'))(), value)
            else:
                self.assertEqual(getattr(doc, prop), value)

    def test_load_from_file_like(self):
        with open(self.dmca_pdf, 'rb') as fp:
            doc = Document(fp)
            self._test_doc_properties(doc)

    def test_load_from_path(self):
        doc = Document(self.dmca_pdf)
        self._test_doc_properties(doc)

    def test_load_pdf_without_xref(self):
        doc = Document(self.simple_file)
        self.assertEqual(1, len(doc))

    def test_document_page_iter(self):
        doc = Document(self.dmca_pdf)
        with self.assertRaises(KeyError):
            doc['abc']
        with self.assertRaises(IndexError):
            doc[-19]
        with self.assertRaises(IndexError):
            doc[18]
        with self.assertRaises(TypeError):
            doc[list()]

        self.assertEqual([], doc[18:])

    def test_document_page_by_label(self):
        doc = Document(self.mandarin_pdf)
        with self.subTest("Test get page by labels"):
            for i in range(len(doc)):
                self.assertEqual(doc[i].index, doc[str(i+1)].index)

    def test_document_text_raw(self):
        doc = Document(self.mandarin_pdf)
        with open(file_in_test_dir('mandarin_first.txt'), 'r', encoding='utf-8') as fp:
            self.assertEqual(doc.text(end=0), fp.read())


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([unittest.makeSuite(DocumentTextCase)])
    return suite


if __name__ == '__main__':
    print('to test use test.py %s' % __file__)
