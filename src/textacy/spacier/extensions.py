import logging
from typing import Dict

import catalogue
from spacy.tokens import Doc

from .. import types


LOGGER = logging.getLogger(__name__)

doc_extensions_registry = catalogue.create("textacy", "doc_extensions")


def get_doc_extensions(name: str) -> Dict[str, Dict[str, types.DocExtFunc]]:
    """
    Get a collection of custom doc extensions that can be set on or removed from
    the global :class:`spacy.tokens.Doc` , specified by ``name`` .

    Note:
        If ``name`` isn't found, you may need to import the module from which it comes.
        For example, the "text_stats" collection of doc extensions is only available
        after running ``import textacy.text_stats`` .
    """
    return doc_extensions_registry.get(name)()


def set_doc_extensions(name: str, force: bool = True):
    """
    Set a collection of custom doc extensions on the global :class:`spacy.tokens.Doc` ,
    specified by ``name`` .

    Args:
        name
        force: If True, set extensions even if existing extensions already exist;
            otherwise, don't overwrite existing extensions.
    """
    for name, kwargs in get_doc_extensions(name).items():
        if not Doc.has_extension(name):
            Doc.set_extension(name, **kwargs)
        elif force is True:
            LOGGER.warning("%s `Doc` extension already exists; overwriting...", name)
            Doc.set_extension(name, **kwargs, force=True)
        else:
            LOGGER.warning(
                "%s `Doc` extension already exists, and was not overwritten", name
            )


def remove_doc_extensions(name: str):
    """
    Remove a collection of custom doc extensions from the global :class:`spacy.tokens.Doc` ,
    specified by ``name`` .
    """
    for name in get_doc_extensions(name).keys():
        _ = Doc.remove_extension(name)
