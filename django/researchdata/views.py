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
                # Options
                option_countby = self.request.GET.get('frequency-countby', '')
                # Query
                output = cwb_exec.frequency(
                    F=query_input,
                    countby=option_countby
                )
                # Process output and add to context
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
                # Options
                # option_countby = self.request.GET.get('ngrams-countby', '')
                option_size = self.request.GET.get('ngrams-size', '')
                # option_frequencythreshold = self.request.GET.get('ngrams-frequencythreshold', '')
                # Query
                output = cwb_exec.ngrams(
                    Context=option_size,
                    query=query_input
                )

                ngrams = {}
                node = u''
                
                # options (temp set, get from client)
                countBy = 'word'
                size = 5
                cs = False
                threshold = 3

                for line in output.splitlines():
                    # print 'line:', line
                    words = [el.rsplit ('/', 1)[countBy == 'lemma' and 1 or 0] for el in line.strip ().split ()]
                    if countBy == 'word':
                        words[size - 1] = words[size - 1][1:]
                    else:
                        words[size - 1] = words[size - 1][:-1]
                    if not cs:
                        words = [w.lower () for w in words]
                    words = tuple (words)
                    for ng in [words[i:i+size] for i in range (len (words) - size + 1)]:
                        if ng in ngrams:
                            ngrams[ng] += 1
                        else:
                            ngrams[ng] = 1
                ngrams = sorted ([[ngram, freq] for ngram, freq in ngrams.items () if freq > threshold], key = lambda x: x[1], reverse = True)

                # print(query)
                print(len(ngrams))
                for ngram in ngrams:
                    word = ngram[0]
                    ngram[0] = ' '.join(word)

                context['query_output'] = ngrams

        return context


class ParallelCorpusView(TemplateView):
    """
    Class-based view to show the Parallel Corpus template
    """
    template_name = 'researchdata/parallel-corpus.html'
