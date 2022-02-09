from django.views.generic import TemplateView
from . import cwb_exec
import re


class MonolingualCorporaInputView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora input template
    """
    template_name = 'researchdata/monolingual-corpora-input.html'


class MonolingualCorporaOutputView(TemplateView):
    """
    Class-based view to show the Monolingual Corpora output template
    """
    template_name = 'researchdata/monolingual-corpora-output.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        output_type = self.request.GET.get('outputtype', '')
        query_input = self.request.GET.get('cqpsearchquery', '')

        context['output_type'] = output_type
        context['query_input'] = query_input

        # Requires a query input (otherwise redirect to input page)
        if query_input != '':

            # Search
            if output_type == 'search':
                # Options
                # option_entriesperpage = self.request.GET.get('search-entriesperpage', '')
                # option_displaymode = self.request.GET.get('search-displaymode', '')
                # option_bigsizelimit = self.request.GET.get('search-bigsizelimit', '')
                # option_showmetadata = self.request.GET.get('search-showmetadata', '')
                # Query
                context['query_output'] = cwb_exec.query(
                    A=query_input,
                    length=50
                )

            # Frequency
            if output_type == 'frequency':
                
                # 1. Options
                option_countby = self.request.GET.get('frequency-countby', '')
                
                # 2. Query
                output = cwb_exec.frequency(
                    F=query_input,
                    countby=option_countby
                )
                
                # 3. Process output
                output = output.strip().split(']')[:-1]
                output = [re.sub(" \[.*", "", i).strip().split('\t') for i in output]
                context['query_output'] = output

            # Collocations
            if output_type == 'collocations':
                # Options
                # option_countby = self.request.GET.get('collocations-countby', '')
                option_spanleft = self.request.GET.get('collocations-spanleft', '')
                option_spanright = self.request.GET.get('collocations-spanright', '')
                # option_frequencythreshold = self.request.GET.get('collocations-frequencythreshold', '')
                # option_llr = self.request.GET.get('collocations-llr', '')
                # option_mi = self.request.GET.get('collocations-mi', '')
                # option_tscore = self.request.GET.get('collocations-tscore', '')
                # option_zscore = self.request.GET.get('collocations-zscore', '')
                # option_dice = self.request.GET.get('collocations-dice', '')
                # option_mi3 = self.request.GET.get('collocations-mi3', '')
                # option_frequency = self.request.GET.get('collocations-frequency', '')
                # Query
                context['query_output'] = cwb_exec.collocations(
                    LeftContext=option_spanleft,
                    RightContext=option_spanright,
                    query=query_input
                )

            # N-grams
            if output_type == 'ngrams':
                
                # 1. Options
                option_countby = self.request.GET.get('ngrams-countby', '')
                option_size = int(self.request.GET.get('ngrams-size', 3))
                option_frequencythreshold = int(self.request.GET.get('ngrams-frequencythreshold', 3))
                
                # 2. Query
                output = cwb_exec.ngrams(
                    Context=option_size,
                    query=query_input
                )
                
                # 3. Process output
                ngrams = {}
                node = u''
                cs = True if '%c' in query_input.split(']')[0] else false  # Case sensitity, from first/primary query
                # Build ngrams
                for line in output.splitlines():
                    words = [el.rsplit('/', 1)[option_countby == 'lemma' and 1 or 0] for el in line.strip().split()]
                    if not cs:
                        words = [w.lower () for w in words]
                    words = tuple (words)
                    for ng in [words[i:i+option_size] for i in range (len(words) - option_size + 1)]:
                        if ng in ngrams:
                            ngrams[ng] += 1
                        else:
                            ngrams[ng] = 1
                # Sort ngrams
                ngrams = sorted ([[ngram, freq] for ngram, freq in ngrams.items () if freq > option_frequencythreshold], key = lambda x: x[1], reverse = True)
                # Process ngram words lists
                for ngram in ngrams:
                    ngram[0] = ' '.join(ngram[0])  # Convert list of words to string
                    ngram[0] = re.sub("<(\S*)|(\S*)>", r"<strong>\1</strong>", ngram[0])  # Wrap query word in strong tags
                context['query_output'] = ngrams

        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'
