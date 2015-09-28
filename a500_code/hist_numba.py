import numba
import numpy as np

# nopython=True means an error will be raised
# if fast compilation is not possible.
@numba.jit(nopython=True)
def fill_counts(y_centers,x_centers,y_indices,x_indices,hist_array):
    """
          given bincenters for each row and column, and row_indices and
          col_indices from searchsorted that give the row,col index of
          each binned data point, return the counts in each 2d bin_col

          input:  row_centers, col_centers   -- vectors giving the location
                  of the center of each bin_col

                  row_indices, col_indices  -- vectors giving the bin that
                  every data point belongs in

                  hist_array  -- the output array holding the counts -- this
                   needs to be declared outside

          output:  hist_array  -- 2d array of shape [len(row_centers),len(col_centers)]
                  containing the number of datapoints that are in each row,column bin_column
                  If there are no datapoints in a bin then the bin contains np.nan
    """
    num_xbins=x_centers.shape[0]
    num_ybins=y_centers.shape[0]
    num_y=y_indices.shape[0]
    for n in range(num_y): #y_indices and x_indices both size of raw data
        if x_indices[n] > 0 and y_indices[n] > 0 and \
            x_indices[n] <= num_xbins and y_indices[n] <= num_ybins:
            bin_row=y_indices[n]-1 # '-1' to get the index of the bin center
            bin_col=x_indices[n]-1
            hist_array[bin_row, bin_col] += 1
    rows,cols=hist_array.shape
    for row in range(rows):
        for col in range(cols):
            if hist_array[row,col] < 1.:
                hist_array[row,col]=np.nan
    return hist_array

            
def hist2d(x_raw,y_raw,x_edges,y_edges):
    """
      Produce a 2-d histogram (for example, of temperature (y) vs.
        vertical velocity (x) data)  binned into temperature,wvel
        bins
      input: row_raw,col_raw: data vectors of the row variable (temperature)
             and the column variable (wvel)
             col_edges, row_edges:  coordinates of the bin edges for each variables
      returns:  counts,col_centers,row_centers

      Example, given 10,000 temperature measurements to be binned into 20 bins, and
               20,000 wvel measurements to be binned into 10 bins, return
               counts as a [20,10]  array with the number of measurements that fall
               into each bin
    """
    print('in numba 6')
    x_centers=(x_edges[:-1] + x_edges[1:])/2.
    y_centers=(y_edges[:-1] + y_edges[1:])/2.
    num_xbins=int(len(x_centers))
    num_ybins=int(len(y_centers))
    x_indices=np.asarray(np.searchsorted(x_edges, x_raw.flat, 'right'),dtype=np.int64)
    y_indices=np.asarray(np.searchsorted(y_edges, y_raw.flat, 'right'),dtype=np.int64)
    hist_array=np.zeros([num_ybins, num_xbins], dtype=np.float)
    hist_array=fill_counts(y_centers,x_centers,y_indices,x_indices,hist_array)
    return hist_array,x_centers,y_centers

