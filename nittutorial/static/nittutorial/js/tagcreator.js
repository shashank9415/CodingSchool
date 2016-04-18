$('#search-text').tagsInput({
				width: 'auto',
				onChange: function(elem, elem_tags)
				{
					var languages = ['dp','tree','stack'];
					$('.tag', elem_tags).each(function()
					{
						if($(this).text().search(new RegExp('\\b(' + languages.join('|') + ')\\b')) >= 0)
							$(this).css('background-color', 'yellow');
					});
				}
			});