;(function($) {
    $.fn.formset = function(opts) {
        var options = $.extend({}, $.fn.formset.defaults, opts),
            flatExtraClasses = options.extraClasses.join(' '),
            totalForms = $('#id_' + options.prefix + '-TOTAL_FORMS'),
            maxForms = $('#id_' + options.prefix + '-MAX_NUM_FORMS'),
            childElementSelector = 'input,select,textarea,label,div',
            $$ = $(this),

            applyExtraClasses = function(row, ndx) {
                if (options.extraClasses) {
                    row.removeClass(flatExtraClasses);
                    row.addClass(options.extraClasses[ndx % options.extraClasses.length]);
                }
            },

            updateElementIndex = function(elem, prefix, ndx) {
                var idRegex = new RegExp(prefix + '-(\\d+|__prefix__)-'),
                    replacement = prefix + '-' + ndx + '-';
                if (elem.attr("for")) elem.attr("for", elem.attr("for").replace(idRegex, replacement));
                if (elem.attr('id')) elem.attr('id', elem.attr('id').replace(idRegex, replacement));
                if (elem.attr('name')) elem.attr('name', elem.attr('name').replace(idRegex, replacement));
            },

            hasChildElements = function(row) {
                return row.find(childElementSelector).length > 0;
            },

            showAddButton = function() {
                return maxForms.length == 0 || (maxForms.val() == '' || (maxForms.val() - totalForms.val() > 0));
            };

        $$.each(function(i) {
            var row = $(this);
            if (hasChildElements(row)) {
                row.addClass(options.formCssClass);
                applyExtraClasses(row, i);
            }
        });

        if ($$.length) {
            var hideAddButton = !showAddButton(),
                addButton, template;
            if (options.formTemplate) {
                template = (options.formTemplate instanceof $) ? options.formTemplate : $(options.formTemplate);
                template.removeAttr('id').addClass(options.formCssClass + ' formset-custom-template');
                template.find(childElementSelector).each(function() {
                    updateElementIndex($(this), options.prefix, '__prefix__');
                });
            } else {
                if (options.hideLastAddForm) $('.' + options.formCssClass + ':last').hide();
                template = $('.' + options.formCssClass + ':last').clone(true).removeAttr('id');
                template.find(childElementSelector).not(options.keepFieldValues).each(function() {
                    var elem = $(this);
                    if (elem.is('input:checkbox') || elem.is('input:radio')) {
                        elem.attr('checked', false);
                    } else {
                        elem.val('');
                    }
                });
            }
            options.formTemplate = template;

            var addButtonHTML = '<a class="' + options.addCssClass + '" href="javascript:void(0);">' + options.addText + '</a>';
            if (options.addContainerClass) {
                var addContainer = $('[class*="' + options.addContainerClass + '"');
                addContainer.append(addButtonHTML);
                addButton = addContainer.find('[class="' + options.addCssClass + '"]');
            } else if ($$.is('TR')) {
                var numCols = $$.eq(0).children().length,
                    buttonRow = $('<tr><td colspan="' + numCols + '">' + addButtonHTML + '</tr>').addClass(options.formCssClass + '-add');
                $$.parent().append(buttonRow);
                addButton = buttonRow.find('a');
            } else {
                $$.filter(':last').after(addButtonHTML);
                addButton = $$.filter(':last').next();
            }

            if (hideAddButton) addButton.hide();

            addButton.click(function() {
                var formCount = parseInt(totalForms.val()),
                    row = options.formTemplate.clone(true).removeClass('formset-custom-template'),
                    buttonRow = $($(this).parents('tr.' + options.formCssClass + '-add').get(0) || this);
                applyExtraClasses(row, formCount);
                row.insertBefore(buttonRow).show();
                row.find(childElementSelector).each(function() {
                    updateElementIndex($(this), options.prefix, formCount);
                });
                totalForms.val(formCount + 1);
                if (!showAddButton()) buttonRow.hide();
                if (options.added) options.added(row);
                return false;
            });
        }

        return $$;
    };

    $.fn.formset.defaults = {
        prefix: 'form',
        formTemplate: null,
        addText: 'add another',
        addContainerClass: null,
        addCssClass: 'add-row',
        formCssClass: 'dynamic-form',
        extraClasses: [],
        keepFieldValues: '',
        added: null,
        hideLastAddForm: false
    };
})(jQuery);
